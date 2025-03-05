import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def demo_search_lte_rating(rating: float):
    result = {
        "count": 0,
        "matched_professors": {}
    }
    searching_rule = {
        "range": {
            "avgRating": {
                "lte": rating
            }
        }
    }
    count_query = {"query": searching_rule}
    query_size = es.count(index="professors", body=count_query )["count"]
    query = {"query": searching_rule,"size": query_size}
    result["count"] = query_size

    # A simple demonstration
    res = es.search(index = "professors", body = query)
    # print("Which professors have rating that less than or equal to 2.0?")
    # print(f"Total count: {query_size}")
    for doc in res["hits"]["hits"]:
        sourse = doc['_source']
        # print(f"A professor at Department {sourse['department']}: {sourse['avgRating']}")
        # Just in case of privacy concern
        # print(f"{sourse['firstName']} {sourse['lastName']}: {sourse['avgRating']}")
        result["matched_professors"][sourse['legacyId']] = {"name": f"{sourse['firstName']} {sourse['lastName']}", "avg_rating": sourse['avgRating']}

    return result

def demo_search_desc_department(department: str):
    result = {
        "count": 0,
        "matched_professors": []
    }
    searching_rule = {
        "match": {
            "department": department
        }
    }
    count_query = {"query": searching_rule}
    query_size = es.count(index="professors", body=count_query )["count"]
    query = {
        "query": searching_rule,"size": query_size,
        "sort": [
            {
                "avgRating": "desc"
            }
        ]
    }
    result["count"] = query_size

    res = es.search(index = "professors", body = query)
    for doc in res["hits"]["hits"]:
        sourse = doc['_source']
        result["matched_professors"].append({"name": f"{sourse['firstName']} {sourse['lastName']}", "department": sourse['department'], "avg_rating": sourse['avgRating']})

    return result