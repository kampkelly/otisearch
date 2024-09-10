from fastapi import APIRouter
from src.apis.v1 import route_setting, route_search, route_user, route_sync

api_router = APIRouter()
api_router.include_router(route_setting.router, prefix="/api/v1/settings", tags=["settings"])
api_router.include_router(route_search.router, prefix="/api/v1/search", tags=["search"])
api_router.include_router(route_user.router, prefix="/api/v1/user", tags=["user"])
api_router.include_router(route_sync.router, prefix="/api/v1/sync", tags=["sync"])
