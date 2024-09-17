from dotenv import load_dotenv
from fastapi import Depends
from src.database.repository import DatabaseRepository, DataSyncRepository, UserRepository
import src.helpers.response as response
from src.lib.esearch.query import ESearchQuery
from src.database.schemas.search_schema import SemanticSearch
from src.lib.base import LLMType
from src.lib.query_generator import QueryGenerator

load_dotenv()


class SearchService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository), database_repository: DatabaseRepository = Depends(DatabaseRepository), datasync_repository: DataSyncRepository = Depends(DataSyncRepository)):
        self.user_repository = user_repository
        self.database_repository = database_repository
        self.datasync_repository = datasync_repository
        # self.sql_generator = QueryGenerator(llm_type, **kwargs)
        self.sql_generator = QueryGenerator(LLMType.OPENAI)
        self.sql_generator.setup()

    def start_semantic_search(self, data: SemanticSearch, user_id: str):
        datasync = self.datasync_repository.get_datasync_by_id(data.datasync_id, user_id)
        all_columns = datasync.tables[0].es_columns
        columns = all_columns.get("columns", [])
        related_columns = all_columns.get("relationships", [])

        query = self.sql_generator.generate_query(data.query, columns, related_columns)
        search_response = self._semantic_search(query, datasync.es_index)

        return response.success_response({"data": search_response})

    def _semantic_search(self, query: str, index_name: str):
        combined_query = {
          "size": 50,
          **query
        }

        esearch = ESearchQuery()
        res = esearch.semantic_Search(index_name, combined_query)

        return {'response': res}
