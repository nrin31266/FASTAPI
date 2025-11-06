from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
from src import models, schemas
from src.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post("/blog"
        #   , response_model=schemas.Blog
          )
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, content=blog.content, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/")
def greet():
    return {"message": "Hello, World! This is the main page."}

@app.get("/about")
def about():
    return {"message": "This is the about page..."}

@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/blog/{id}")
def blog_post(id: int):
    return {"message": f"This is blog post number {id}"}

@app.get("/blog")
def blog_list(limit: int = 5, offset: int = 0, published: bool = True):
    #  21 blog static fixed data
    blogs = [
    
        {"id": 1, "title": "Blog Post 1", "published": True},
        {"id": 2, "title": "Blog Post 2", "published": False},
        {"id": 3, "title": "Blog Post 3", "published": True},
        {"id": 4, "title": "Blog Post 4", "published": True},
        {"id": 5, "title": "Blog Post 5", "published": False},
        {"id": 6, "title": "Blog Post 6", "published": True},
        {"id": 7, "title": "Blog Post 7", "published": True},
        {"id": 8, "title": "Blog Post 8", "published": False},
        {"id": 9, "title": "Blog Post 9", "published": True},
        {"id": 10, "title": "Blog Post 10", "published": True},
        {"id": 11, "title": "Blog Post 11", "published": False},
        {"id": 12, "title": "Blog Post 12", "published": True},
        {"id": 13, "title": "Blog Post 13", "published": True},
        {"id": 14, "title": "Blog Post 14", "published": False},
        {"id": 15, "title": "Blog Post 15", "published": True},
        {"id": 16, "title": "Blog Post 16", "published": True},
        {"id": 17, "title": "Blog Post 17", "published": False},
        {"id": 18, "title": "Blog Post 18", "published": True},
        {"id": 19, "title": "Blog Post 19", "published": True},
        {"id": 20, "title": "Blog Post 20", "published": False},
    ]
    filtered_blogs = [blog for blog in blogs if blog["published"] == published]
    return filtered_blogs[offset : offset + limit]

@app.get("/blog/{id}/comments")
def blog_comments(id: int):
    return {"message": f"Comments for blog post {id}", "comments": [ "Great post!", "Very informative.", "Thanks for sharing!" ]}

# if __name__ == "__main__":
#     run(app, host="0.0.0.0", port=8089)
