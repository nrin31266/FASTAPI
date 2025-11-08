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

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=ApiResponse[dto.UserResponse])
def login(user: dto.LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise BaseException(BaseErrorCode.NOT_FOUND, message="User not found")

    if not verify_password(user.password, db_user.hashed_password):
        raise BaseException(BaseErrorCode.UNAUTHORIZED, message="Invalid credentials")

    return ApiResponse.success(data=db_user)

