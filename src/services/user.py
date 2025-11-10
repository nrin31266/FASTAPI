# from sqlalchemy.orm import Session
# from src import dto, models
# from src.repositories import blog as blog_repository
# from src.errors.base_exception import BaseException
# from src.errors.base_error_code import BaseErrorCode
# from src.repositories import user as user_repository
# # from src.utils.security import hash_password, verify_password
# from src.keycloak_auth.dto import UserPrincipal


# def get_user_by_keycloak_id(db: Session, keycloak_id: str) -> models.User | None:
#     user = user_repository.get_by_keycloak_id(db, keycloak_id)
#     return user

# def get_or_create_user(db: Session, rq: UserPrincipal) -> models.User:
#     user = user_repository.get_by_keycloak_id(db, rq.sub)
#     if user:
#         return user
#     user = models.User(
#         keycloak_id=rq.sub,
#         email=rq.email,
#         first_name=rq.first_name,
#         last_name=rq.last_name
#     )
#     return user_repository.create(db, user)
