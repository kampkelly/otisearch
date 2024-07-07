from typing import Union, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from src.database.session import get_db
import src.database.repository.setting as setting_repository
import src.helpers.response as response

import src.lib.llama.search as search

router = APIRouter()


class SchemaInput(BaseModel):
    databaseName: str
    tableName: str
    columns: List[str]


class SimilaritiesInput(BaseModel):
    text: str
    email: EmailStr


@router.get("/word")
def get_search_word(q: Union[str, None] = None):
    result = search.get_search_word(q)
    return {"word": result}


@router.post("/similarities")
def similarities(body: SimilaritiesInput, db: Session = Depends(get_db)):
    existing_setting = setting_repository.get_setting_by_email(body.email, db)
    if not existing_setting:
        return response.error_response('setting does not exist', 404)
    result = search.similarities(body.text, existing_setting)
    return result
