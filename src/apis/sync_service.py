import os
from dotenv import load_dotenv
from fastapi import Depends
from src.database.schemas.sync_schema import AddDatabase, TriggerSync
from src.database.repository import DatabaseRepository, DataSyncRepository, UserRepository
import src.helpers.response as response
from src.apis.sync_database_service import SyncDatabaseConnection
from src.utils.create_schema_json import create_json_file
from pgsync.index import PGSync
from src.utils.index import parse_postgres_url, generate_index_name
from src.lib.esearch.query import ESearchQuery

load_dotenv()


class SyncService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository), database_repository: DatabaseRepository = Depends(DatabaseRepository), datasync_repository: DataSyncRepository = Depends(DataSyncRepository)):
        self.user_repository = user_repository
        self.database_repository = database_repository
        self.datasync_repository = datasync_repository

    def compare_relationships(self, relationships, compare):
        error_messages = []
        for relationship in relationships:
            found = False
            for item in compare:
                if item["column"] == relationship["foreign_key"]:
                    found = True
                    if relationship["type"] and item.get("type"):
                        if relationship["type"] != item["type"]:
                            error_messages.append(f"Type mismatch for {relationship['name']}: {relationship['type']} != {item['type']}")
                    compare_columns = [col["name"] for col in item["columns"]]
                    missing_columns = [col for col in relationship["columns"] if col not in compare_columns]

                    if missing_columns:
                        error_messages.append(f"Missing columns in {relationship['name']}: {missing_columns}")

            if not found:
                error_messages.append(f"No matching foreign_table found for {relationship['name']}.")

        if error_messages:
            raise ValueError("\n".join(error_messages))

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
        tables_list = await db_conn.get_schema_info()
        found_table = tables_list.get(data.table, None)

        if not found_table:
            return response.error_response(f'Table "{data.table}" not found in database', 404)
        columns = found_table["columns"]

        if data.columns:
            if not all(col in [c['name'] for c in columns] for col in data.columns):
                return response.error_response("One or more specified columns do not exist in the table", 404)
            columns = data.columns

        new_database = existing_database

        self.compare_relationships(data.relationships, found_table["relationships"])
        if not existing_database:
            new_database = self.database_repository.create_new_database(data, user_id)
        table_data = {
            "table_name": data.table,
            "columns": columns,
            "relationships": data.relationships
        }
        # create datasync
        new_datasync = self.datasync_repository.create_new_datasync({
            "es_index": generate_index_name(data.database_name, data.table),
            "is_active": False
        },
            user_id)
        new_table = self.database_repository.create_new_table(table_data, new_database.id, new_datasync.id)

        database_with_new_table = self.database_repository.get_database_with_table(new_database.id, new_table.id, user_id)
        return response.success_response(database_with_new_table)

    async def get_database_info(self, postgres_url: str, table: str):
        db_conn = SyncDatabaseConnection(postgres_url)
        tables_list = await db_conn.get_schema_info()
        selected_table = tables_list.get(table, [])
        if not selected_table:
            return response.error_response("Table not found", 404)
        return response.success_response({table: selected_table})

    async def get_databases(self, user_id: str):
        databases = self.database_repository.get_databases(user_id)
        return response.success_response({"databases": databases})

    async def trigger_sync(self, data: TriggerSync, user_id: str):
        datasync = self.datasync_repository.get_datasync_by_id(data.datasync_id, user_id)

        _, file_path = create_json_file(
            database=datasync.tables[0].database.database_name,
            table=datasync.tables[0].table_name,
            es_index=datasync.es_index,
            columns=datasync.tables[0].columns,
            relationships=datasync.tables[0].relationships
        )

        parsed_postgres_url = parse_postgres_url(datasync.tables[0].database.postgres_url)

        pgsync_envs = {
            "PG_USER": parsed_postgres_url["PG_USER"],
            "PG_HOST": parsed_postgres_url["PG_HOST"],
            "PG_PORT": parsed_postgres_url["PG_PORT"],
            "PG_PASSWORD": parsed_postgres_url["PG_PASSWORD"],
            "PG_SSLMODE": "",
            "ELASTICSEARCH_CLOUD_ID": os.getenv('ELASTICSEARCH_CLOUD_ID', ""),
            "ELASTICSEARCH_API_KEY": os.getenv('ELASTICSEARCH_API_KEY', ""),
            "ELASTICSEARCH_PORT": os.getenv('ELASTICSEARCH_PORT', ""),
        }

        pgsync = PGSync(pgsync_envs, file_path, datasync.es_index)
        pgsync.start_sync()
        pgsync.list_processes("running")

        return response.success_response(datasync)

    async def sync_status(self, data: TriggerSync, user_id: str):
        datasync = self.datasync_repository.get_datasync_by_id(data.datasync_id, user_id)

        db_conn = SyncDatabaseConnection(datasync.tables[0].database.postgres_url)
        table_row_count = await db_conn.get_table_row_count(datasync.tables[0].table_name)

        esearch = ESearchQuery()
        index_count, is_success = esearch.get_index_row_count(datasync.es_index)

        percent_completed = int((index_count / table_row_count * 100)) if table_row_count > 0 else 0

        resp = {
            "table_row_count": table_row_count,
            "es_index_count": index_count,
            "is_success": is_success,
            "percent": percent_completed,
        }

        return response.success_response(resp)
