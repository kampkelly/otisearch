from typing import Union, List
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from src.database.session import get_db
from fastapi import APIRouter, Depends, status
import src.database.repository.setting as setting_repository
import src.helpers.response as response
from src.database.schemas.search_schema import SemanticSearch
import src.lib.llama.search as search
from src.utils.auth import verify_token
from src.apis.search_service import SearchService

router = APIRouter()


class SchemaInput(BaseModel):
    databaseName: str
    tableName: str
    columns: List[str]


class SimilaritiesInput(BaseModel):
    text: str
    email: EmailStr
    llm_check: bool = False


@router.get("/word")
def get_search_word(q: Union[str, None] = None):
    result = search.get_search_word(q)
    return {"word": result}


@router.post("/similarities")
def similarities(body: SimilaritiesInput, db: Session = Depends(get_db)):
    existing_setting = setting_repository.get_setting_by_email(body.email, db)
    if not existing_setting:
        return response.error_response('setting does not exist', 404)
    result = search.similarities_with_voyage(body.text, existing_setting, body.llm_check)
    return result


@router.post("/semantic", status_code=status.HTTP_200_OK)
def semantic_search(data: SemanticSearch, search_service: SearchService = Depends(SearchService), user_id: str = Depends(verify_token)):
    try:
        resp = search_service.start_semantic_search(data, user_id)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")
