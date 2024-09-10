from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.models.database import Database
from src.database.session import get_db


class DatabaseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_database_by_id(self, id: str, user_id: str):
        database = self.db.query(Database).filter(
            Database.id == id,
            Database.user_id == user_id
        ).first()
        return database
