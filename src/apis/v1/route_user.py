from src.helpers.response import UserResponse, LoginResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.apis.user import User
from src.database.schemas.user_schema import UserCreate, UserLogin

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_account(user: UserCreate, db: Session = Depends(get_db)):
    response = User.create_user_account(user=user, db=db)
    return response


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    response = User.login_user(user=user, db=db)
    return response
