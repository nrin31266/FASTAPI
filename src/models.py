from src.database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    creator = relationship("User", back_populates="blogs")
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    blogs = relationship("Blog", back_populates="creator")
    
