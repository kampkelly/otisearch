from fastapi import Depends
from src.database.schemas.user_schema import UserCreate, CompleteInfo
from src.database.repository import DatabaseRepository
from src.database.repository import UserRepository
import src.helpers.response as response


class SyncService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    def add_database(self, user_id: str, data: UserCreate):
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            return response.error_response('user does not exist', 403)

        if data.database_id:
            print('>>>>>dbbbb')
            # existing_database = DatabaseRepository.get_database_by_id(data.database_id, user_id, db)
      
        return response.success_response({})
