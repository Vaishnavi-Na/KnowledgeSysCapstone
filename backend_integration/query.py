import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def search_professors_sort(subject: str, courseNum: str, sort_by: str = None, order: str = 'desc', comment_keywords: str = None):
    demo_result = {
        "count": 0,
        "matched_professors": {}
    }

    valid_sort_fields = ['SEI', 'avg_rating', 'difficulty', 'comments_relevance']
    if sort_by and sort_by not in valid_sort_fields:
        raise ValueError(f"Invalid sort_by field: {sort_by}. Valid options are {valid_sort_fields}")

    should_clauses = [
        {
            "bool": {
                "must": [
                    {"match": {"SEI.Subject": subject}},
                    {"match": {"SEI.Catalog": courseNum}}
                ]
            }
        },
        {"match": {"Ratings.course": subject.upper() + courseNum}}
    ]

    # Add full-text keyword match in comments if requested
    if comment_keywords:
        should_clauses.append({
            "match": {
                "comments_overview": {
                    "query": comment_keywords,
                    "boost": 3  # Give it a nice boost to push relevant profs up
                }
            }
        })

    query = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        },
        "size": 7000
    }

    # Add sorting by numeric fields
    if sort_by and sort_by != "comments_relevance":
        es_field = {
            "SEI": "SEI.Overall",
            "avg_rating": "avgRating",
            "difficulty": "avgDifficulty"
        }[sort_by]
        query["sort"] = [{es_field: {"order": order}}]

    # Perform the search
    res = es.search(index="professors", body=query)

    matched = {}
    for result in res["hits"]["hits"]:
        source = result['_source']
        matched[result['_id']] = {
            "name": f"{source['firstName']} {source['lastName']}",
            "avg_rating": source.get('avgRating'),
            "difficulty": source.get('avgDifficulty'),
            "SEI": source.get('SEI'),
            "comments_overview": source.get("comments_overview", ""),
            "score": result.get('_score')  # Save score for relevance sorting
        }

    # Sort locally by ES relevance if sorting by comments_relevance
    if sort_by == "comments_relevance":
        reverse = (order == 'desc')
        matched = dict(sorted(matched.items(), key=lambda item: item[1].get("score", 0), reverse=reverse))

    demo_result["matched_professors"] = matched
    demo_result["count"] = len(matched)
    return demo_result

# results = demo_search_course("math", "1148")
# for result in results["matched_professors"]:
#     print(results["matched_professors"][result])
#     print("Name:", results["matched_professors"][result]['name'])
#     print("Average Rating:", results["matched_professors"][result]['avg_rating'])
#     print("Average Difficulty:", results["matched_professors"][result]['difficulty'])
#     print("SEI:", results["matched_professors"][result]['SEI'])
#     print()
