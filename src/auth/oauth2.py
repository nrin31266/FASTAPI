from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from .token import decode_token
#  Annotated
from typing import Annotated



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = BaseException(
        BaseErrorCode.UNAUTHORIZED,
        message="Could not validate credentials",
    )
    user = decode_token(token, credentials_exception)
    return user