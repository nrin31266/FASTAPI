from passlib.context import CryptContext
import logging 
# Khởi tạo context dùng thuật toán bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu"""
    logging.info("Hashing password: %s", password)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh mật khẩu gốc với mật khẩu đã mã hóa"""
    return pwd_context.verify(plain_password, hashed_password)
