import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import ssl

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

index_name = "professors"

# Scan all documents
docs = scan(es, index=index_name)

count_fixed = 0
count_deleted = 0
count_skipped = 0

for doc in docs:
    _id = doc["_id"]
    source = doc["_source"]
    
    first = source.get("firstName", "")
    last = source.get("lastName", "")
    if not first or not last:
        print(f"Skipping record with missing name: {_id}")
        count_skipped += 1
        continue

    expected_id = f"{last}{first}"
    
    if _id == expected_id:
        continue  # Already correct

    # Check if correct ID already exists
    try:
        existing = es.get(index=index_name, id=expected_id)
        # Correct ID already exists, delete this one
        es.delete(index=index_name, id=_id)
        print(f"Deleted duplicate record: {_id} (correct one already exists: {expected_id})")
        count_deleted += 1
    except:
        # Correct ID doesn't exist, reindex with correct ID and delete old one
        es.index(index=index_name, id=expected_id, document=source)
        es.delete(index=index_name, id=_id)
        print(f"Fixed record ID: {_id} -> {expected_id}")
        count_fixed += 1

print(f"\nCleanup done. {count_fixed} fixed, {count_deleted} deleted, {count_skipped} skipped.")
