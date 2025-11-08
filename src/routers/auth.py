from fastapi import APIRouter, status
from src import dto, models
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.dto import ApiResponse
from typing import Optional
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.utils.security import verify_password
from src.services import auth as auth_service
from src.auth import dto as auth_dto
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# @router.post("/login", response_model=ApiResponse[auth_dto.Token])
# def login(user: dto.LoginRequest, db: Session = Depends(get_db)):
#     authenticated_user = auth_service.login(db, user)
#     return ApiResponse.success(data=authenticated_user, message="Login successful")


@router.post("/login", response_model=auth_dto.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    authenticated_user = auth_service.login(db, user)
    return authenticated_user

