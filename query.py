from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import ssl
from dotenv import load_dotenv
import os



#Setup elasticsearch through REST API library
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

indices = es.indices.get_alias(index="*")
for index_name in indices:
    print(index_name)

es.indices.delete(index="courses", ignore_unavailable=True)