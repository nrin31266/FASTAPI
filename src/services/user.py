from sqlalchemy.orm import Session
from src import dto, models
from src.repositories import blog as blog_repository
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode
from src.repositories import user as user_repository
from src.utils.security import hash_password, verify_password



def create(db: Session, request: dto.UserCreateRequest) -> models.User:
    user = models.User(**request.model_dump(exclude={"password"}))
    user.hashed_password = hash_password(request.password)
    return user_repository.create(db, user)
    
def get_by_id(db: Session, user_id: int) -> models.User:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"User with id {user_id} not found")
    return user