from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import ssl
import os

# Delete all professors (for testing index updates)
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))


resp = es.delete_by_query(
    index="professors",
    query={
        "match_all": {}
    },
)
print(resp)