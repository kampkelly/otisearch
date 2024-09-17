from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload, contains_eager
from src.database.models.database import Database
from src.database.models.table import Table
from src.database.session import get_db
from src.database.schemas.sync_schema import AddDatabase


class DatabaseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_database_by_id(self, id: str, user_id: str):
        database = self.db.query(Database).filter(
            Database.id == id,
            Database.user_id == user_id
        ).first()
        return database

    def get_database_by_url(self, url: str, user_id: str):
        database = self.db.query(Database).filter(
            Database.postgres_url == url,
            Database.user_id == user_id
        ).first()
        return database

    def create_new_database(self, databaseData: AddDatabase, user_id: str):
        database = Database(
            postgres_url=databaseData.postgres_url,
            database_name=databaseData.database_name,
            user_id=user_id
        )
        self.db.add(database)
        self.db.commit()
        self.db.refresh(database)
        return database

    def create_new_table(self, tableData: Table, database_id: str, datasync_id: str):
        rel = [rel.to_dict() for rel in tableData["relationships"]]

        table = Table(
            table_name=tableData["table_name"],
            columns=tableData["columns"],
            relationships=rel,
            database_id=database_id,
            datasync_id=datasync_id
        )
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def update_table(self, table_id: str, tableData: dict):
        table = self.db.query(Table).filter(Table.id == table_id).first()
        if table:
            for key, value in tableData.items():
                if hasattr(table, key):
                    setattr(table, key, value)
            self.db.commit()
            self.db.refresh(table)
            return table
        return None

    def get_tables_by_database_id(self, database_id: str) -> List[Table]:
        tables = self.db.query(Table).filter(Table.database_id == database_id).all()
        return tables

    def get_table_by_name_and_database_id(self, table_name: str, database_id: str) -> Table:
        table = self.db.query(Table).filter(
            Table.table_name == table_name,
            Table.database_id == database_id
        ).first()
        return table

    def get_database_with_table(self, database_id: str, table_id: str, user_id: str):
        database = self.db.query(Database).outerjoin(
            Database.tables
        ).options(
            contains_eager(Database.tables)
        ).filter(
            Database.id == database_id,
            Database.user_id == user_id,
            Table.id == table_id
        ).first()
        return database

    def get_database_with_tables(self, database_id: str, user_id: str):
        database = self.db.query(Database).options(
            joinedload(Database.tables)
        ).filter(
            Database.id == database_id,
            Database.user_id == user_id
        ).first()

        return database

    def get_databases(self, user_id: str):
        databases = self.db.query(Database).options(
            joinedload(Database.tables)
        ).filter(
            Database.user_id == user_id
        ).all()
        return databases
