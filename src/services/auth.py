from sqlalchemy.orm import Session
from src import dto, models
from src.repositories import blog as blog_repository
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.repositories import user as user_repository
from src.utils.security import hash_password, verify_password
from datetime import timedelta
from src.auth.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.auth import dto as auth_dto
from fastapi.security import OAuth2PasswordRequestForm

# def login(db: Session, request: dto.LoginRequest) -> auth_dto.Token:
#     user = db.query(models.User).filter(models.User.email == request.email).first()
#     if not user or not verify_password(request.password, user.hashed_password):
#         raise BaseException(BaseErrorCode.UNAUTHORIZED, message="Invalid email or password")
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email, "role": ["default", "fastapi"]}, expires_delta=access_token_expires
#     )

#     return auth_dto.Token(access_token=access_token, token_type="bearer")

def login(db: Session, request: OAuth2PasswordRequestForm) -> auth_dto.Token:
    user = db.query(models.User).filter(models.User.email == request.username).first() # Note: request.username holds the email
    if not user or not verify_password(request.password, user.hashed_password):
        raise BaseException(BaseErrorCode.UNAUTHORIZED, message="Invalid email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "roles": ["default", "fastapi"]}, expires_delta=access_token_expires
    )

    return auth_dto.Token(access_token=access_token, token_type="bearer")