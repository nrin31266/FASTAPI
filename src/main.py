# main.py

import logging
from typing import Optional
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from uvicorn import run
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src import models, dto
from src.database import engine, get_db
from sqlalchemy.orm import Session

from src.errors.base_exception_handler import (
    base_exception_handler,
    global_exception_handler,
    http_exception_handler
)
from src.errors.base_exception import BaseException
from src.routers import product_router
from src.eureka_client.eureka_config import (
    register_with_eureka,
)  # Đảm bảo import này đúng
from src.kafka.consumer import start_kafka_consumers
from src.kafka.producer import periodic_flush, producer
# StarletteHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

import asyncio

# --- 1. Cấu hình logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


# --- 2. Định nghĩa Lifespan (cho Eureka) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Khi app START ---
    await register_with_eureka()
    print("✅ Registered with Eureka")
    # asyncio.create_task(start_kafka_consumers())
    # print("📡 Kafka consumers started")
    # Khởi chạy Kafka consumers trong background
    kafka_task = asyncio.create_task(start_kafka_consumers())
    flush_task = asyncio.create_task(periodic_flush())  # Thêm periodic flush
    
    print("📡 Kafka consumers started")
    yield  # 👉 FastAPI chạy trong khoảng này

     # --- Khi app SHUTDOWN ---
    print("🧹 Shutting down FastAPI...")
    kafka_task.cancel()
    flush_task.cancel()
    try:
        await kafka_task
        await flush_task
    except asyncio.CancelledError:
        pass
    producer.flush(10)  # Flush cuối cùng


# --- 3. Tạo FastAPI App (CHỈ MỘT LẦN) ---
app = FastAPI(
    title="FastAPI Service",
    lifespan=lifespan,
)

# --- 4. Thêm Middleware (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 6. Include các Routers ---
app.include_router(product_router.router)
# app.include_router(blog.router)
# app.include_router(user.router)
# app.include_router(auth.router)

# --- 5. Đăng ký Exception Handlers ---
app.add_exception_handler(BaseException, base_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# --- 7. Tạo các bảng CSDL ---
models.Base.metadata.create_all(bind=engine)


# --- 8. Thêm các route gốc (Health check, Info) ---
@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/info")
def info():
    return {"service": "inventory-service", "version": "1.0.0"}
