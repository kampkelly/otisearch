from sqlalchemy.orm import Session

from src.database.schemas.user_schema import UserCreate
import src.database.repository.user as user_repository
import src.helpers.response as response


class User:
    @staticmethod
    def create_user_account(user: UserCreate, db: Session):
        existing_user = user_repository.get_user_by_email(user.email, db)
        if existing_user:
            return response.error_response('email already exists', 403)

        new_user = user_repository.create_new_user(user, db)
        return new_user
