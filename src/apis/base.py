from fastapi import APIRouter
from src.apis.v1 import route_setting

api_router = APIRouter()
api_router.include_router(route_setting.router, prefix="/api/v1/settings", tags=["settings"])
