from fastapi import APIRouter, status
from src import dto
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.dto import ApiResponse
from src.services import user as user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("", response_model=ApiResponse[dto.UserResponse])
def create_user(rq: dto.UserCreateRequest, db: Session = Depends(get_db)):
    user = user_service.create(db, rq)
    return ApiResponse.success(data=user)

@router.get("/{id}", response_model=ApiResponse[dto.UserResponse])
def get_user(id: int, db: Session = Depends(get_db)):
    user = user_service.get_by_id(db, id)
    return ApiResponse.success(data=user)