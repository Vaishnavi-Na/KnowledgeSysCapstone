import os
import random
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import ssl
import json

# Set up SSL context
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT

# Load environment variables
load_dotenv()
es = Elasticsearch(
    'https://localhost:9200',
    ssl_context=ctx,
    basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD'))
)

# Use scan helper to retrieve all docs from the index
docs = list(scan(es, index="professors"))

# Print 5 random professor records
print("Sample professor records:")
for prof in random.sample(docs, 5):
    print(json.dumps(prof['_source'], indent=2, ensure_ascii=False))
    print("-" * 60)