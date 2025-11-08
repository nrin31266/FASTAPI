from sqlalchemy.orm import Session
from src import models, dto

def get_all_blogs(db: Session):
    return db.query(models.Blog).all()

def get_blog_by_id(blog_id: int, db: Session):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def create_blog(blog: models.Blog, db: Session):
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def delete_blog(blog: models.Blog, db: Session):
    db.delete(blog)
    db.commit()

def update_blog(blog_model: models.Blog, blog_dto: dto.BlogCreateRequest, db: Session):
    """
    Cập nhật 1 blog model từ 1 blog DTO.
    Đây là cách an toàn hơn là dùng __dict__.
    """
    # Cập nhật các trường từ DTO
    blog_model.title = blog_dto.title
    blog_model.content = blog_dto.content
    blog_model.published = blog_dto.published
    
    # Commit thay đổi
    db.commit()
    db.refresh(blog_model)
    return blog_model