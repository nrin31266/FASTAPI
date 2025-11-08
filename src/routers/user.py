from fastapi import APIRouter, status
from src import dto, models
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.dto import ApiResponse
from typing import Optional
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.utils.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("", response_model=ApiResponse[dto.UserResponse], tags=["users"])
def create_user(user: dto.UserCreateRequest, db: Session = Depends(get_db)):
    # new_user = models.User(
    #     username=user.username,
    #     email=user.email,
    #     hashed_password=user.password  # Lưu ý: Trong thực tế, bạn nên hash mật khẩu trước khi lưu
    # )
    new_user = models.User(**user.model_dump(exclude={"password"}))
    new_user.hashed_password = hash_password(user.password) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ApiResponse.success(data=new_user)

@router.get("/{id}", response_model=ApiResponse[dto.UserResponse])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"User with id {id} not found")
    return ApiResponse.success(data=user)