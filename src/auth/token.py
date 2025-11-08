SECRET_KEY = "a9f5d7e6c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from src.auth import dto as auth_dto
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
import logging 


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT token - placeholder function"""
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str, credentials_exception: BaseException) -> auth_dto.UserPrincipal:
    """Giải mã JWT token - placeholder function"""
    logging.info(f"Decoding token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        roles: list[str] = payload.get("roles", [])
        if email is None:
            raise JWTError("Invalid token: missing subject")
        return auth_dto.UserPrincipal(email=email, roles=roles)
    except JWTError as e:
        logging.error(f"Error decoding token: {e}")
        raise credentials_exception from e