from src.helpers.response import UserResponse, LoginResponse, CompleteInfoResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.apis.user import User
from src.database.schemas.user_schema import UserCreate, UserLogin, CompleteInfo
from src.utils.auth import verify_token

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_account(user: UserCreate, db: Session = Depends(get_db)):
    response = User.create_user_account(user=user, db=db)
    return response


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    response = User.login_user(user=user, db=db)
    return response


@router.post("/complete-info", response_model=CompleteInfoResponse, status_code=status.HTTP_200_OK)
def complete_info(info: CompleteInfo, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    response = User.complete_info(user_id=user_id, info=info, db=db)
    return response
