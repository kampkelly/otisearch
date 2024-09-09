from sqlalchemy.orm import Session
from src.database.schemas.user_schema import UserCreate
from src.database.models.user import User
from src.utils.index import hash_password


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


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
