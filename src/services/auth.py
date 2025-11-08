from sqlalchemy.orm import Session
from src import dto, models
from src.repositories import blog as blog_repository
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.repositories import user as user_repository
from src.utils.security import hash_password, verify_password

def login(db: Session, request: dto.LoginRequest) -> models.User:
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise BaseException(BaseErrorCode.UNAUTHORIZED, message="Invalid email or password")
    return user