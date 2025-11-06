from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

# Tao engine ket noi den database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tao session factory de tuong tac voi database


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False: khong tu dong commit cac thay doi vao database
# autoflush=False: khong tu dong flush cac thay doi vao database
# bind=engine: su dung engine da tao de ket noi den database

# Base class de khai bao cac model
Base = declarative_base()