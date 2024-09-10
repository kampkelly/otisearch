from src.helpers.response import CompleteInfoResponse
from fastapi import APIRouter, Depends, status
from src.apis.sync_service import SyncService
from src.database.schemas.sync_schema import AddDatabase
from src.utils.auth import verify_token

router = APIRouter()


# @router.post("/add-database", response_model=CompleteInfoResponse, status_code=status.HTTP_200_OK)
@router.post("/add-database", status_code=status.HTTP_200_OK)
def add_database(data: AddDatabase, sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    response = sync_service.add_database(user_id=user_id, data=data)
    return response
