from typing import List, Any
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload, contains_eager
from src.database.models.datasync import DataSync
from src.database.models.table import Table
from src.database.session import get_db
from src.database.schemas.sync_schema import AddDatabase


class DataSyncRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_datasync_by_id(self, id: str, user_id: str):
        # datasync = self.db.query(DataSync).filter(
        datasync = self.db.query(DataSync).options(
            joinedload(DataSync.tables).joinedload(Table.database)
        ).filter(
            DataSync.id == id,
            DataSync.user_id == user_id
        ).first()
        return datasync

    def create_new_datasync(self, datasyncData: Any, user_id: str):
        datasync = DataSync(
            es_index=datasyncData["es_index"],
            user_id=user_id,
            is_active=datasyncData["is_active"]
        )
        self.db.add(datasync)
        self.db.commit()
        self.db.refresh(datasync)
        return datasync

    def get_datasyncs(self, user_id: str, is_active: bool):
        query = self.db.query(DataSync).options(
            joinedload(DataSync.tables).joinedload(Table.database)
        ).filter(
            DataSync.user_id == user_id
        )

        if is_active is not None:
            query = query.filter(DataSync.is_active == is_active)

        return query.all()
