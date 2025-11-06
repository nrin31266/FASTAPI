from src.database import Base
from sqlalchemy import Boolean, Column, Integer, String

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)