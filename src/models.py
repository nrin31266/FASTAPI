from datetime import datetime
from src.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Double,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True)
    quantity = Column(Integer)
    price = Column(Double)
    # Tự động tạo khi insert
    created_at = Column(DateTime, default=datetime.now)
    # Tự động cập nhật khi update
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    reserved_orders = relationship(
        "ReservedOrder",
        back_populates="product",
        cascade="all, delete-orphan",  # Tự động xóa reserved_orders khi xóa product
    )


class ReservedOrder(Base):
    __tablename__ = "reserved_orders"

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    order_id = Column(Integer, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")
    
class MediaAudio(Base):
    __tablename__ = "media_audios"
    id = Column(Integer, primary_key=True, index=True)
    input_url = Column(String, nullable=False)
    input_type = Column(String, nullable=False)  # e.g., 'youtube, audio_file'
    file_path = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # duration in seconds
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


# class Blog(Base):
#     __tablename__ = "blogs"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     content = Column(String)
#     published = Column(Boolean, default=True)

#     user_id = Column(String, ForeignKey("users.keycloak_id"))

#     creator = relationship("User", back_populates="blogs")

# class User(Base):
#     __tablename__ = "users"
#     email = Column(String, unique=True, index=True)
#     keycloak_id = Column(String, unique=True, index=True, primary_key=True)
#     first_name = Column(String)
#     last_name = Column(String)

#     blogs = relationship("Blog", back_populates="creator")
