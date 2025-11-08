import logging
from typing import Optional
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from uvicorn import run

from src import models, dto
from src.database import engine, get_db
from sqlalchemy.orm import Session

from src.errors.base_exception_handler import (
    base_exception_handler,
    global_exception_handler,
)
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.dto import ApiResponse
from src.utils.security import hash_password, verify_password
from src.routers import blog, user, auth

# Cấu hình logging cơ bản
logging.basicConfig(
    level=logging.INFO,  # Mức log tối thiểu
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI()

# Đăng ký handler
app.add_exception_handler(BaseException, base_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include routers
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

# CORS configuration (similar to your Spring config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True, # cho phép gửi cookie
    allow_methods=["*"],  # tất cả phương thức
    allow_headers=["*"],  # tất cả header
)

# # ========== KEYCLOAK JWT AUTHENTICATION CONFIGURATION ==========

# from src.auth.dependencies import get_current_user, require_role
# from src.auth.models import User


# # Routes bảo vệ bằng Keycloak JWT - GIỐNG HỆT Spring Security configuration
# @app.get("/api/inventories")
# async def get_inventories(user: User = Depends(get_current_user)):
#     """Tương tự .requestMatchers("/api/inventories").authenticated()"""
#     return {
#         "message": f"Hello {user.username}",
#         "roles": user.roles,
#         "data": ["inventory1", "inventory2"]
#     }

# @app.get("/api/admin")
# async def admin_only(user: User = Depends(require_role("ROLE_ADMIN"))):
#     """Route yêu cầu ROLE_ADMIN"""
#     return {"message": "Admin access granted"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# # anyRequest().authenticated() - tất cả routes cần authentication
# # (Bạn có thể áp dụng dependency cho tất cả routes nếu muốn)