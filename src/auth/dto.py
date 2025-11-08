# from pydantic import BaseModel
# from typing import List

# class User(BaseModel):
#     id: str
#     username: str
#     email: str
#     roles: List[str]


from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
# class TokenData(BaseModel):
#     email: str | None = None

class UserPrincipal(BaseModel):
    email: str 
    roles: list[str] = []
