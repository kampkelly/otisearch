import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from src.database import settings_config

security = HTTPBearer()


def get_token(user_id: str):
    token = jwt.encode({
              'sub': user_id,
              'exp': datetime.now() + timedelta(minutes=30)
          }, settings_config.SECRET_KEY, algorithm='HS256')

    return token


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings_config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
