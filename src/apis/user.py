import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database import settings_config
from src.database.schemas.user_schema import UserCreate
import src.database.repository.user as user_repository
import src.helpers.response as response
from src.utils.index import hash_password


class User:
    @staticmethod
    def create_user_account(user: UserCreate, db: Session):
        existing_user = user_repository.get_user_by_email(user.email, db)
        if existing_user:
            return response.error_response('email already exists', 403)

        new_user = user_repository.create_new_user(user, db)
        return response.success_response(new_user)

    @staticmethod
    def login_user(user: UserCreate, db: Session):
        existing_user = user_repository.get_user_by_email(user.email, db)
        if not existing_user:
            return response.error_response('email or password incorrect', 401)

        if existing_user.password != hash_password(user.password):
            return response.error_response('email or password incorrect', 401)

        token = jwt.encode({
            'sub': existing_user.id,
            'exp': datetime.now() + timedelta(minutes=30)
        }, settings_config.SECRET_KEY, algorithm='HS256')

        return response.success_response({'token': token, "kj": "ok"})
