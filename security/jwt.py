from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer




load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRATION_TIME = int(os.getenv("EXPIRATION_TIME", "30"))


def create_access_token(user_id: int):
    to_encode = {"sub": str(user_id)}

    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)

    to_encode.update({"exp": expire})

    encoded_jwt = encode(
        to_encode,
        JWT_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = decode(
            token,
            JWT_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return int(user_id)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def refresh_access_token(token: str):
    try:
        payload = decode(
            token,
            JWT_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return create_access_token(int(user_id))
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

security = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str):
    return verify_access_token(token)