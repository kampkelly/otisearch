from typing import Any
from sqlalchemy.orm import Session
from src.database.schemas.user_schema import UserCreate
from src.database.models.user import User
from src.utils.index import hash_password


class UserRepository:
    @staticmethod
    def create_new_user(user: UserCreate, db: Session):
        user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_name=user.company_name,
            password=hash_password(user.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(id: int, db: Session):
        user = db.query(User).filter(User.id == id).first()
        return user

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def update_user(id: str, data: Any, db: Session):
        existing_user = UserRepository.get_user_by_id(id, db)
        if not existing_user:
            return None
        for key, value in data.dict().items():
            setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)
        return existing_user
