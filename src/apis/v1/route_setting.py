from typing import Union, List
from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel

from src.database.schemas.setting_schema import SettingCreate, ShowSetting
from src.database.session import get_db
from src.utils import create_schema_json
from src.helpers.response import success_response

import src.apis.settings as settings

router = APIRouter()


class SchemaInput(BaseModel):
    databaseName: str
    tableName: str
    columns: List[str]


@router.post("/", response_model=ShowSetting, status_code=status.HTTP_201_CREATED)
def create_setting(setting: SettingCreate, db: Session = Depends(get_db)):
    setting = settings.create_new_setting(setting=setting, db=db)
    return setting


@router.get("/index-status")
def get_index_status(index: Union[str, None] = None, email: Union[str, None] = None, db: Session = Depends(get_db)):
    result = settings.get_index_status(email=email, db=db)
    return result


@router.post("/create-json")
def create_json(schema_input: SchemaInput):
    create_schema_json.create_json_file(schema_input.databaseName, schema_input.tableName, schema_input.columns)
    return success_response({})
