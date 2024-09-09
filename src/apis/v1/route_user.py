import src.lib.llama.search as search
from src.helpers.response import success_response, UserResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.apis.user import User
from src.database.schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_account(user: UserCreate, db: Session = Depends(get_db)):
    user = User.create_user_account(user=user, db=db)
    return success_response(user)
