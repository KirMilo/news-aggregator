from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", refreshUrl="api/v1/auth/token/refresh")
http_bearer = HTTPBearer()

def verify_token(authorization: HTTPAuthorizationCredentials):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = authorization.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        return user_id
    except JWTError:
        raise credentials_exception


async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return verify_token(authorization)
