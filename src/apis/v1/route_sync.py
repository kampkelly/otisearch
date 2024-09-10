from src.helpers.response import CompleteInfoResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.apis.sync import Sync
from src.database.schemas.sync_schema import AddDatabase
from src.utils.auth import verify_token

router = APIRouter()


# @router.post("/add-database", response_model=CompleteInfoResponse, status_code=status.HTTP_200_OK)
@router.post("/add-database", status_code=status.HTTP_200_OK)
def complete_info(data: AddDatabase, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    response = Sync.add_database(user_id=user_id, data=data, db=db)
    return response
