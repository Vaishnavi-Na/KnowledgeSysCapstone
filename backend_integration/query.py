import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def demo_search_course(subject: str, courseNum: str):
    demo_result = {
        "count": 0,
        "matched_professors": {}
    }
    query = {
        "query": {
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
                    # {"match": {"Ratings.index": "300"}} # Gets all professors with over 300 ratings
                    {"match": {"Ratings.course": subject.upper()+courseNum}} # Gets all professors that have taught the course
                ],
                "minimum_should_match": 1 # Course should be listed in RMP OR SEI
            }
        },
        "size": 7000
    }

    # A simple demonstration
    res = es.search(index = "professors", body=query)
    for doc in res["hits"]["hits"]:
        source = doc['_source']
        demo_result["count"] = demo_result["count"] + 1
        demo_result["matched_professors"][source['legacyId']] = {"name": f"{source['firstName']} {source['lastName']}", "avg_rating": source['avgRating']}

    # print(demo_result)
    return demo_result

print(demo_search_course("math", "1148"))