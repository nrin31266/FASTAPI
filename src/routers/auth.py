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
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=ApiResponse[dto.UserResponse])
def login(user: dto.LoginRequest, db: Session = Depends(get_db)):
    authenticated_user = auth_service.login(db, user)
    return ApiResponse.success(data=authenticated_user, message="Login successful")

