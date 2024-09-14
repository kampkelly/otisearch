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
