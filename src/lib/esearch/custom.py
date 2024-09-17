from langchain.schema import BaseRetriever, Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from typing import List, Any


class CustomElasticsearchRetriever(BaseRetriever):
    index_name: str
    esearch_client: Any
    columns: Any
    related_columns: Any
    generate_query: Any

    def _get_relevant_documents(self, query: Any, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        es_query_json = self.generate_query(query, self.columns, self.related_columns)

        combined_query = {
          "size": 50,
          **es_query_json
        }
        response = self.esearch_client.search(index=self.index_name, body=combined_query)

        documents = []
        for hit in response['hits']['hits']:
            excluded_keys = {'search_vectors'}

            # Combine all columns into a single string for page_content
            page_content = ' '.join(
                f"{key}: {value}"
                for key, value in hit['_source'].items()
                if key not in excluded_keys
            )

            # Include all columns in metadata
            metadata = {
                key: value
                for key, value in hit['_source'].items()
                if key not in excluded_keys
            }

            doc = Document(
                page_content=page_content,
                metadata=metadata
            )
            documents.append(doc)

        return documents

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        raise NotImplementedError("Async retrieval not implemented")
