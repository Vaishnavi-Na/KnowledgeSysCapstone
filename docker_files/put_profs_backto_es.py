import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl
import json

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

index_name = "professors"

index_exists = es.indices.exists(index=index_name)

def find_existing_doc(first_name, last_name):
    if not index_exists:
        return None

    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"firstName": first_name}},
                    {"match": {"lastName": last_name}}
                ]
            }
        }
    }

    res = es.search(index=index_name, query=query["query"], size=1)
    if res["hits"]["hits"]:
        return res["hits"]["hits"][0]  # Return the whole hit (includes _id and _source)
    return None


def update_record(prof):
    first_name = prof["firstName"]
    last_name = prof["lastName"]
    
    existing_hit = find_existing_doc(first_name, last_name)
    
    if existing_hit:
        existing_source = existing_hit["_source"]
        existing_id = existing_hit["_id"]
        
        # Preserve SEI from existing document
        if existing_source.get("SEI"):
            prof["SEI"] = existing_source["SEI"]
        else:
            prof["SEI"] = prof.get("SEI", [])
        
        # Update the existing document
        es.index(index=index_name, id=existing_id, document=prof)
    else:
        # No matching document found, insert as new (let ES assign a new ID)
        prof["SEI"] = prof.get("SEI", [])
        es.index(index=index_name, document=prof, id=last_name + first_name)

    print(f"updated {last_name+first_name}")


# Load and re-upload JSON records from directory
folder_path = "docker_files/profs_sort_by_department"
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            for prof in records:
                update_record(prof)

print("Done putting records back into Elasticsearch.")
