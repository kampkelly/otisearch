import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from src.database import settings_config
from uuid import UUID
from src.database.repository import UserRepository

security = HTTPBearer()


def get_token(user_id: UUID):
    token = jwt.encode({
              'sub': str(user_id),
              'exp': datetime.now() + timedelta(minutes=30)
          }, settings_config.SECRET_KEY, algorithm='HS256')

    return token


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security),  user_repository: UserRepository = Depends(UserRepository)):
    try:
        payload = jwt.decode(credentials.credentials, settings_config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
