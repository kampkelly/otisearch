from fastapi import Depends
from src.database.schemas.sync_schema import AddDatabase
from src.database.repository import DatabaseRepository
from src.database.repository import UserRepository
import src.helpers.response as response
from src.apis.sync_database_service import SyncDatabaseConnection


class SyncService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository), database_repository: DatabaseRepository = Depends(DatabaseRepository)):
        self.user_repository = user_repository
        self.database_repository = database_repository

    async def add_database(self, user_id: str, data: AddDatabase):
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            return response.error_response("user does not exist", 403)

        existing_database = None
        found_table = None
        postgres_url = data.postgres_url
        if data.database_id:
            existing_database = self.database_repository.get_database_by_id(data.database_id, user_id)
            if existing_database:
                postgres_url = existing_database.postgres_url

        if not existing_database:
            existing_database = self.database_repository.get_database_by_url(postgres_url, user_id)

        if existing_database:
            existing_table = self.database_repository.get_table_by_name_and_database_id(data.table, existing_database.id)
            if existing_table:
                return response.error_response("Table has already been added", 403)
        db_conn = SyncDatabaseConnection(postgres_url)
        tables_list = await db_conn.get_tables()
        found_table = data.table if data.table in tables_list else None

        if not found_table:
            return response.error_response('Table not found in database', 404)
        columns = await db_conn.get_columns(data.table)

        if data.columns:
            if not all(col in columns for col in data.columns):
                return response.error_response("One or more specified columns do not exist in the table", 404)
            columns = data.columns

        new_database = existing_database
        if not existing_database:
            new_database = self.database_repository.create_new_database(data, user_id)
        table_data = {
            "table_name": data.table,
            "columns": columns,
            "es_index": "random"
        }
        new_table = self.database_repository.create_new_table(table_data, new_database.id)
        
        database_with_new_table = self.database_repository.get_database_with_table(new_database.id, new_table.id, user_id)
        return response.success_response(database_with_new_table)

    async def get_database_info(self, postgres_url: str, table: str):
        db_conn = SyncDatabaseConnection(postgres_url)
        tables_list = await db_conn.get_schema_info()
        selected_table = tables_list.get(table, [])
        if not selected_table:
            return response.error_response("Table not found", 404)
        return response.success_response({table: selected_table})
