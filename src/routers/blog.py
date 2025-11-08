from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import Optional

from src import dto
from src.database import get_db
from src.dto import ApiResponse
from src.services import blog as blog_service, user as user_service # <--- THAY ĐỔI: Import service
# from src.repositories import blog as blog_repository # <--- KHÔNG DÙNG REPO Ở ĐÂY
from src.keycloak_auth.dto import UserPrincipal
from src.keycloak_auth.dependencies import get_current_user, require_roles



router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.get("", response_model=ApiResponse[list[dto.BlogResponse]])
def get_blogs(db: Session = Depends(get_db), current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"]))):
    # Chỉ gọi service
    blogs = blog_service.get_all(db)
    
    return ApiResponse.success(data=blogs)

@router.post("", 
            response_model=ApiResponse[dto.BlogResponse], 
            status_code=status.HTTP_201_CREATED)
def create_blog(blog: dto.BlogCreateRequest, db: Session = Depends(get_db), current_user: UserPrincipal = Depends(get_current_user)):
    exitsting_user = user_service.get_or_create_user(db, current_user)
    
    # Chỉ gọi service, logic tạo model đã bị dời đi
    new_blog = blog_service.create(blog, exitsting_user.keycloak_id, db)
    return ApiResponse.success(data=new_blog, message="Blog created successfully")

# Sửa lỗi: Bỏ "/blog" vì đã có prefix="/blog"
@router.get("/{id}", response_model=ApiResponse[dto.BlogResponse])
def get_blog(id: int, db: Session = Depends(get_db), current_user: UserPrincipal = Depends(get_current_user)):
    # Chỉ gọi service. Logic 'if not blog' đã bị dời đi
    blog = blog_service.get_by_id(id, db)
    return ApiResponse.success(data=blog)

@router.delete("/{id}", response_model=ApiResponse[Optional[dto.BlogResponse]],)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: UserPrincipal = Depends(get_current_user)):
    # Chỉ gọi service. Logic 'if not blog' đã bị dời đi
    blog_service.delete(id, db)
    return ApiResponse.success(message=f"Blog with id {id} deleted successfully")

@router.put("/{id}", response_model=ApiResponse[dto.BlogResponse])
def update_blog(id: int, updated_blog: dto.BlogCreateRequest, db: Session = Depends(get_db), current_user: UserPrincipal = Depends(get_current_user)):
    # Chỉ gọi service. Logic 'if not blog' đã bị dời đi
    blog = blog_service.update(id, updated_blog, db)
    return ApiResponse.success(data=blog, message="Blog updated successfully")