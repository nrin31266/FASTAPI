from fastapi import APIRouter, status
from src import dto
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.dto import ApiResponse
from src.services import user as user_service
import src.keycloak_auth.dto as auth_dto
from src.keycloak_auth.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# @router.post("", response_model=ApiResponse[dto.UserResponse])
# def create_user(rq: dto.UserCreateRequest, db: Session = Depends(get_db)):
#     user = user_service.create(db, rq)
#     return ApiResponse.success(data=user)

@router.get("/{keycloak_id}", response_model=ApiResponse[dto.UserResponse])
def get_user(keycloak_id: str, db: Session = Depends(get_db)):
    user = user_service.get_by_keycloak_id(db, keycloak_id)
    return ApiResponse.success(data=user)

@router.post("", response_model=ApiResponse[dto.UserResponse])
def my_profile(db: Session = Depends(get_db), current_user: auth_dto.UserPrincipal = Depends(get_current_user)):
    user = user_service.get_or_create_user(db, current_user)
    return ApiResponse.success(data=user)