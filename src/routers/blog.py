from fastapi import APIRouter, status
from src import dto, models
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.dto import ApiResponse
from typing import Optional
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode


router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.get("", response_model= ApiResponse[list[dto.BlogResponse]]
            # , tags=["blogs"]
            )
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return ApiResponse.success(data=blogs)
@router.post(""
          , response_model= ApiResponse[dto.BlogResponse]
          , status_code= status.HTTP_201_CREATED
          , tags=["blogs"])
def create_blog(blog: dto.BlogCreateRequest, db: Session = Depends(get_db), user_id: int = 1):
    new_blog = models.Blog(title=blog.title, content=blog.content, published=blog.published, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return ApiResponse.success(dto.BlogResponse.model_validate(new_blog))


@router.get("/blog/{id}", response_model= ApiResponse[dto.BlogResponse], tags=["blogs"])
def get_blog(id: int, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with id {id} not found")
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")
    return ApiResponse.success(data=blog)


@router.delete("/blog/{id}", response_model= ApiResponse[Optional[dto.BlogResponse]], tags=["blogs"])
def delete_blog(id: int, db: Session = Depends(get_db), ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if(not blog):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with id {id} not found")
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return ApiResponse.success(message=f"Blog with id {id} deleted successfully")

@router.put("/blog/{id}", response_model=ApiResponse[dto.BlogResponse], tags=["blogs"])
def update_blog(id: int, updated_blog: dto.BlogCreateRequest, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    existing_blog = blog_query.first()
    if not existing_blog:
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {id} not found")

    # ✅ chuyển Pydantic → dict
    blog_query.update(updated_blog.model_dump(), synchronize_session=False)
    db.commit()

    updated = blog_query.first()
    return ApiResponse.success(data=dto.BlogResponse.model_validate(updated))
