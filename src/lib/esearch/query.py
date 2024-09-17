from typing import Any
from src.lib.esearch.index import ESearch


class ESearchQuery:
    def __init__(self):
        self.esearch_client = ESearch().client

    def get_index_row_count(self, index_name: str):
        response = self.esearch_client.count(index=index_name)
        cat_response = self.esearch_client.cat.indices(index=index_name, format="json")

        if response:
            is_success = response['count'] and response['_shards']['successful'] and cat_response[0]["health"] == "green"
            return response['count'], is_success
        raise ValueError(f"Index '{index_name}' not found.")

    def _process_es_results(self, es_response):
        nodes = []
        for hit in es_response['hits']['hits']:
            source = hit['_source']
            score = hit['_score']

            node = dict(source)
            node.pop('search_vectors', None)

            node['score'] = score

            nodes.append(node)

        return nodes

    def semantic_Search(self, index_name: str, body: Any):
        response = self.esearch_client.search(index=index_name, body=body)
        if response:
            res = self._process_es_results(response)
            return {"count": len(res), "response": res}
        return {"count": None, "response": []}
