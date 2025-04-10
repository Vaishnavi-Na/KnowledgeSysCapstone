import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import ssl
import json

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

# Use scan helper to retrieve all docs from the index
docs = scan(es, index="professors")

# Group courses by subject
department_groups = {}
for doc in docs:
    source = doc['_source']
    department = source.get("department", "UNKNOWN")
    department_groups.setdefault(department, []).append(source)

# Save each subject group into its own JSON file
for subject, courses in department_groups.items():
    filename = f"{subject}.json"
    with open(f"docker_files/profs_sort_by_department/{filename}", 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)

print("Done exporting courses by department.")