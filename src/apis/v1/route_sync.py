from src.helpers.response import AddDatabaseResponse
from fastapi import APIRouter, Depends, status
from src.apis.sync_service import SyncService
from src.database.schemas.sync_schema import AddDatabase, TriggerSync
from src.utils.auth import verify_token
import src.helpers.response as response

router = APIRouter()


@router.post("/add-database", response_model=AddDatabaseResponse, status_code=status.HTTP_201_CREATED)
async def add_database(data: AddDatabase, sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    try:
        resp = await sync_service.add_database(user_id=user_id, data=data)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")


@router.get("/database-info", status_code=status.HTTP_200_OK)
async def get_database_info(postgres_url: str, table: str, sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    try:
        resp = await sync_service.get_database_info(postgres_url=postgres_url, table=table)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")


@router.get("/databases", status_code=status.HTTP_200_OK)
async def get_databases(sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    try:
        resp = await sync_service.get_databases(user_id)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")


@router.post("/trigger-sync", status_code=status.HTTP_200_OK)
async def trigger_sync(data: TriggerSync, sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    try:
        resp = await sync_service.trigger_sync(data, user_id)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")


@router.post("/status", status_code=status.HTTP_200_OK)
async def sync_status(data: TriggerSync, sync_service: SyncService = Depends(SyncService), user_id: str = Depends(verify_token)):
    try:
        resp = await sync_service.sync_status(data, user_id)
        return resp
    except Exception as e:
        return response.error_response(f"{e}")
