from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel  # 👈 THÊM DÒNG NÀY
# import List
from typing import List
T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):  # 👈 ĐỔI BaseModel → GenericModel
    code: int = Field(default=200, description="Mã code ứng dụng")
    message: Optional[str] = Field(default="Success", description="Thông điệp kết quả")
    result: Optional[T] = Field(default=None, description="Dữ liệu trả về")

    @classmethod
    def success(cls, data: Optional[T] = None, message: str = "Success"):
        """Factory method tương tự trong Java"""
        return cls(code=200, message=message, result=data or None)

    @classmethod
    def error(cls, code: int, message: str):
        """Factory method cho lỗi chung"""
        return cls(code=code, message=message)

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user_id: int
    
    creator: "User"
    class Config:
        from_attributes = True
        
class Blog(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int  
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class BlogCreateRequest(BaseModel):
    title: str
    content: str
    published: bool = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    blogs : "List[Blog]"

    class Config:
        from_attributes = True
        

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str