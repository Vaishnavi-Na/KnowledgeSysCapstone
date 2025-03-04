import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def demo_search(rating: float):
    demo_result = {
        "count": 0,
        "matched_professors": {}
    }
    count_query = {
        "query": {
            "range": {
                "avgRating": {
                    "lte": rating
                }
            }
        }
    }
    query_size = es.count(index="professors", body=count_query )["count"]
    query = {
        "query": {
            # "match": {
            #     "department": "English"
            # }
            "range": {
                "avgRating": {
                    "lte": rating
                }
            }
        },
        "size": query_size
    }
    demo_result["count"] = query_size

    # A simple demonstration
    res = es.search(index = "professors", body = query)
    # print("Which professors have rating that less than or equal to 2.0?")
    # print(f"Total count: {query_size}")
    for doc in res["hits"]["hits"]:
        sourse = doc['_source']
        # print(f"A professor at Department {sourse['department']}: {sourse['avgRating']}")
        # Just in case of privacy concern
        # print(f"{sourse['firstName']} {sourse['lastName']}: {sourse['avgRating']}")
        demo_result["matched_professors"][sourse['legacyId']] = {"name": f"{sourse['firstName']} {sourse['lastName']}", "avg_rating": sourse['avgRating']}

    return demo_result
