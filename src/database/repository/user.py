from typing import Any
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.schemas.user_schema import UserCreate
from src.database.models.user import User
from src.utils.index import hash_password
from src.database.session import get_db


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_new_user(self, user: UserCreate):
        user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_name=user.company_name,
            password=hash_password(user.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, id: str):
        user = self.db.query(User).filter(User.id == id).first()
        return user

    def get_user_by_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def update_user(self, id: str, data: Any):
        existing_user = self.get_user_by_id(id)
        if not existing_user:
            return None
        for key, value in data.dict().items():
            setattr(existing_user, key, value)
        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user
