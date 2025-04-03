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
docs = scan(es, index="osu_courses")

# Group courses by subject
subject_groups = {}
for doc in docs:
    source = doc['_source']
    course_field = source.get("course", "")
    subject = course_field.split()[0] if course_field else "UNKNOWN"
    subject_groups.setdefault(subject, []).append(source)

# Save each subject group into its own JSON file
for subject, courses in subject_groups.items():
    filename = f"{subject}.json"
    with open(f"docker_files/prereqs_sort_by_subject/{filename}", 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)

print("Done exporting courses by subject.")