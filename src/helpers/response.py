from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.database.schemas.user_schema import ShowUser


def success_response(data):
    return {"status": "success", "data": data}


def error_response(message: str, status_code: int = 400):
    return JSONResponse(content={"status": "error", "message": message}, status_code=status_code)


class BaseResponse(BaseModel):
    status: str


class UserResponse(BaseModel):
    status: str
    data: ShowUser


class LoginData(BaseModel):
    token: str


class LoginResponse(BaseModel):
    status: str
    data: LoginData


class CompleteInfoData(BaseModel):
    purpose: str


class CompleteInfoResponse(BaseModel):
    status: str
    data: CompleteInfoData
