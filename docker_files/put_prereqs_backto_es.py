import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import ssl
import json

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

index_name = "osu_courses"
data_dir = "docker_files/prereqs_sort_by_subject/"

# Create index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    print(f"Created index: {index_name}")
else:
    print(f"Index already exists: {index_name}")

# Read all JSON files and bulk insert documents
actions = []
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
            courses = json.load(f)
            for course in courses:
                actions.append({
                    "_index": index_name,
                    "_source": course
                })

# Bulk upload to Elasticsearch
if actions:
    success, _ = bulk(es, actions)
    print(f"Successfully indexed {success} documents.")
else:
    print("No documents to index.")