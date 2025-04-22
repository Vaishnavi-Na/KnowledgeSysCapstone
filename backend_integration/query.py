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
        "matched_professors": []
    }

    valid_sort_fields = ['sei', 'avg_rating', 'difficulty', 'comments_relevance']
    if sort_by and sort_by not in valid_sort_fields:
        raise ValueError(f"Invalid sort_by field: {sort_by}. Valid options are {valid_sort_fields}")

    must_clause = {
        "bool": {
            "should": [
                {
                    "bool": {
                        "must": [
                            {"match": {"SEI.Subject": subject}},
                            {"match": {"SEI.Catalog": courseNum}}
                        ]
                    }
                },
                {"match": {"Ratings.course": subject.upper() + courseNum}}
            ],
            "minimum_should_match": 1
        }
    }

    # Add full-text keyword match in comments if requested
    should_clause = []
    if comment_keywords:
        should_clause.append({
            "match": {
                "summary_comment": {
                    "query": comment_keywords,
                    "boost": 3  # Give it a nice boost to push relevant profs up
                }
            }
        })

    query = {
        "query": {
            "bool": {
                "must": must_clause,
                "should": should_clause  # this is for boosting only
            }
        },
        "size": 7000
    }

    # Add sorting by numeric fields
    if sort_by in ['avg_rating', 'difficulty']:
        es_field = {
            "avg_rating": "avgRating",
            "difficulty": "avgDifficulty"
        }[sort_by]
        query["sort"] = [{es_field: {"order": order}}]

    # Perform the search
    res = es.search(index="professors", body=query)

    matched_list = []
    for result in res["hits"]["hits"]:
        source = result['_source']
        # Filter and average relevant SEI ratings
        sei_entries = source.get("SEI", [])
        relevant_ratings = [
            float(entry["Rating"])
            for entry in sei_entries
            if entry.get("Subject") == subject and entry.get("Catalog") == courseNum and "Rating" in entry
        ]
        sei_avg = round(sum(relevant_ratings) / len(relevant_ratings), 2) if relevant_ratings else None

        matched_list.append({
            "id": result['_id'],
            "name": f"{source['firstName']} {source['lastName']}",
            "avg_rating": source.get('avgRating'),
            "difficulty": source.get('avgDifficulty'),
            "SEI_overall": sei_avg,
            "SEI": sei_entries,
            "summary_comment": source.get("summary_comment", ""),
            "score": result.get('_score')  # Save score for relevance sorting
        })

    # Apply local sorting if SEI or comments relevance is the chosen method
    reverse = (order == 'desc')
    if sort_by == "sei":
        matched_list.sort(key=lambda prof: (prof["SEI_overall"] is not None, prof["SEI_overall"]), reverse=reverse)
    elif sort_by == "comments_relevance":
        matched_list.sort(key=lambda prof: prof.get("score", 0), reverse=reverse)

    demo_result["matched_professors"] = matched_list
    demo_result["count"] = len(matched_list)
    return demo_result

# results = search_professors_sort("math", "1148")
# for result in results["matched_professors"]:
#     print(result)
#     print(f"Name:{result['name']}")
#     print(f"Average Rating:{result['avg_rating']}")
#     print(f"Average Difficulty:{result['difficulty']}")
#     print(f"SEI:{result['SEI']}")
#     print()
