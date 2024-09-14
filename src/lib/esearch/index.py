import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class ESearch():
    def __init__(self):
        cloud_id = os.getenv('ELASTICSEARCH_CLOUD_ID', "")
        api_key = os.getenv('ELASTICSEARCH_API_KEY', "")

        self.client = Elasticsearch(
            cloud_id=cloud_id,
            api_key=api_key
        )
