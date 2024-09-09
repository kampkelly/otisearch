from typing import Union, List
from pydantic import BaseModel, EmailStr, Field


class SettingCreate(BaseModel):
    email: EmailStr
    db_user: str
    db_name: str
    db_password: str
    db_host: str
    db_port: int
    db_table: str
    db_schema: str
    columns: List[str]


class ShowSetting(BaseModel):
    id: int
    email: EmailStr
    secret_key: str
    db_user: str
    db_name: str
    db_host: str
    db_port: int
    db_table: str
    db_schema: str
    es_index: str

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
