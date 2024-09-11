from uuid import UUID
from typing import List, Optional
from datetime import datetime
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


class TableInfo(BaseModel):
    es_index: str
    database_id: UUID
    columns: List[str]
    created_at: datetime
    table_name: str
    id: UUID
    updated_at: Optional[datetime] = None


class DatabaseInfo(BaseModel):
    id: UUID
    datasync_id: Optional[UUID] = None
    postgres_url: str
    updated_at: Optional[datetime] = None
    user_id: UUID
    created_at: datetime
    database_name: str
    tables: List[TableInfo]


class AddDatabaseResponse(BaseModel):
    status: str
    data: DatabaseInfo
