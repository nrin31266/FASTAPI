from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
from src import models, dto
from src.database import engine, SessionLocal
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
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

@app.post("/blog"
          , response_model= ApiResponse[dto.BlogResponse]
          , status_code= status.HTTP_201_CREATED)
def create_blog(blog: dto.BlogCreateRequest, db: Session = Depends(get_db), ):
    new_blog = models.Blog(title=blog.title, content=blog.content, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return ApiResponse.success(dto.BlogResponse.from_orm(new_blog))

@app.get("/blog", response_model= ApiResponse[list[dto.BlogResponse]])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return ApiResponse.success(data=blogs)

@app.get("/blog/{id}", response_model= ApiResponse[dto.BlogResponse])
def get_blog(id: int, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with id {id} not found")
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")
    return ApiResponse.success(data=blog)


@app.delete("/blog/{id}", response_model= ApiResponse[Optional[dto.BlogResponse]])
def delete_blog(id: int, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with id {id} not found")
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return ApiResponse.success(message=f"Blog with id {id} deleted successfully")

@app.put("/blog/{id}", response_model= ApiResponse[dto.BlogResponse])
def update_blog(id: int, updated_blog: dto.BlogCreateRequest, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")
    blog.title = updated_blog.title
    blog.content = updated_blog.content
    blog.published = updated_blog.published
    db.commit()
    db.refresh(blog)
    return ApiResponse.success(data=blog)
