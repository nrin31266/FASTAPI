import logging

# Cấu hình logging cơ bản
logging.basicConfig(
    level=logging.INFO,  # Mức log tối thiểu
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
from src import models, dto
from src.database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, Response, HTTPException
app = FastAPI()

from src.errors.base_exception_handler import (
    base_exception_handler,
    global_exception_handler,
)
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode

# Đăng ký handler
app.add_exception_handler(BaseException, base_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
# Import ApiResponse
from src.dto import ApiResponse

# hash
from src.utils.security import hash_password, verify_password

# iclude routers
from src.routers import blog, user, auth
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)




models.Base.metadata.create_all(bind=engine)



