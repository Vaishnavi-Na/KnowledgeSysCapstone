import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

count_query = {
    "query": {
        "range": {
            "avgRating": {
                "lte": 2.0
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
                "lte": 2.0
            }
        }
    },
    "size": query_size
}

# A simple demonstration
res = es.search(index = "professors", body = query)
print("Which professors have rating that less than or equal to 2.0?")
print(f"Total count: {query_size}")
for doc in res["hits"]["hits"]:
    sourse = doc['_source']
    print(f"A professor at Department {sourse['department']}: {sourse['avgRating']}")
    # Just in case of privacy concern
    # print(f"{sourse['firstName']} {sourse['lastName']}: {sourse['avgRating']}")
