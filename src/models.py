from src.database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)

    user_id = Column(String, ForeignKey("users.keycloak_id"))

    creator = relationship("User", back_populates="blogs")
    
class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    keycloak_id = Column(String, unique=True, index=True, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
    blogs = relationship("Blog", back_populates="creator")
    
