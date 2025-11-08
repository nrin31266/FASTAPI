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
# app.include_router(auth.router)

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






