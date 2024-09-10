from fastapi import Depends
from src.database.schemas.user_schema import UserCreate, CompleteInfo
from src.database.repository import UserRepository
import src.helpers.response as response
from src.utils.index import hash_password
from src.utils.auth import get_token
from uuid import UUID


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    def create_user_account(self, user: UserCreate):
        existing_user = self.user_repository.get_user_by_email(user.email)
        if existing_user:
            return response.error_response('email already exists', 403)

        new_user = self.user_repository.create_new_user(user)
        return response.success_response(new_user)

    def login_user(self, user: UserCreate):
        existing_user = self.user_repository.get_user_by_email(user.email)
        if not existing_user:
            return response.error_response('email or password incorrect', 401)

        if existing_user.password != hash_password(user.password):
            return response.error_response('email or password incorrect', 401)

        token = get_token(existing_user.id)

        return response.success_response({'token': token, "kj": "ok"})

    def complete_info(self, user_id: UUID, info: CompleteInfo):
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            return response.error_response('user not found', 404)

        updated_user = self.user_repository.update_user(user_id, info)
        return response.success_response(updated_user)
