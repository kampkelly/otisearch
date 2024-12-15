import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class ESearch():
    def __init__(self):
        es_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
        es_port = int(os.getenv("ELASTICSEARCH_PORT", 9200))
        es_scheme = os.getenv("ELASTICSEARCH_SCHEME", "http")

        self.client = Elasticsearch(
            hosts=[{'host': es_host, 'port': es_port, 'scheme': es_scheme}]
        )
