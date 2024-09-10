from sqlalchemy.orm import Session
from src.database.schemas.user_schema import UserCreate, CompleteInfo
from src.database.repository.user import UserRepository
import src.helpers.response as response
from src.utils.index import hash_password
from src.utils.auth import get_token


class User:
    @staticmethod
    def create_user_account(user: UserCreate, db: Session):
        existing_user = UserRepository.get_user_by_email(user.email, db)
        if existing_user:
            return response.error_response('email already exists', 403)

        new_user = UserRepository.create_new_user(user, db)
        return response.success_response(new_user)

    @staticmethod
    def login_user(user: UserCreate, db: Session):
        existing_user = UserRepository.get_user_by_email(user.email, db)
        if not existing_user:
            return response.error_response('email or password incorrect', 401)

        if existing_user.password != hash_password(user.password):
            return response.error_response('email or password incorrect', 401)

        token = get_token(existing_user.id)

        return response.success_response({'token': token, "kj": "ok"})

    @staticmethod
    def complete_info(user_id: str, info: CompleteInfo, db: Session):
        existing_user = UserRepository.get_user_by_id(user_id, db)
        if not existing_user:
            return response.error_response('user not found', 404)

        updated_user = UserRepository.update_user(user_id, info, db)
        return response.success_response(updated_user)
