from sqlalchemy.orm import Session
from src.database.schemas.user_schema import UserCreate, CompleteInfo
from src.database.repository.user import UserRepository
import src.helpers.response as response


class Sync:
    @staticmethod
    def add_database(user_id: str, data: UserCreate, db: Session):
        existing_user = UserRepository.get_user_by_id(user_id, db)
        if existing_user:
            return response.error_response('user does not exist', 403)

        # new_user = UserRepository.create_new_user(user, db)
        return response.success_response({})
