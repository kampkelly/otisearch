from src.helpers.response import UserResponse, LoginResponse, CompleteInfoResponse
from fastapi import APIRouter, Depends, status
from src.apis.user_service import UserService
from src.database.schemas.user_schema import UserCreate, UserLogin, CompleteInfo
from src.utils.auth import verify_token

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_account(user: UserCreate, user_service: UserService = Depends(UserService)):
    response = user_service.create_user_account(user=user)
    return response


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, user_service: UserService = Depends(UserService)):
    response = user_service.login_user(user=user)
    return response


@router.post("/complete-info", response_model=CompleteInfoResponse, status_code=status.HTTP_200_OK)
def complete_info(info: CompleteInfo, user_service: UserService = Depends(UserService), user_id: str = Depends(verify_token)):
    response = user_service.complete_info(user_id=user_id, info=info)
    return response
