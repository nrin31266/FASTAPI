from sqlalchemy.orm import Session
from src import dto, models
from src.repositories import blog as blog_repository
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode

def get_all(db: Session) -> list[models.Blog]:
    """
    Service để lấy tất cả blogs.
    (Hiện tại chỉ gọi repo, nhưng sau này có thể thêm logic phân trang...)
    """
    return blog_repository.get_all_blogs(db) 

def get_by_id(blog_id: int, db: Session) -> models.Blog:
    """
    Service để lấy 1 blog theo ID.
    Chứa logic nghiệp vụ là kiểm tra blog có tồn tại không.
    """
    blog = blog_repository.get_blog_by_id(blog_id, db)
    if not blog:
        # Logic kiểm tra "not found" nằm ở đây, không nằm ở router
        raise BaseException(BaseErrorCode.NOT_FOUND, message=f"Blog with id {blog_id} not found")
    return blog

def create(blog_dto: dto.BlogCreateRequest, keycloak_id: str, db: Session) -> models.Blog:
    """
    Service để tạo blog mới.
    Chứa logic tạo đối tượng model từ DTO.
    """
    # Logic tạo model nằm ở đây
    new_blog = models.Blog(
        title=blog_dto.title, 
        content=blog_dto.content, 
        published=blog_dto.published, 
        user_id=keycloak_id
    )
    
    # Gọi repo để lưu
    return blog_repository.create_blog(new_blog, db)

def delete(blog_id: int, db: Session, ) -> None:
    """
    Service để xóa 1 blog.
    Chứa logic kiểm tra tồn tại trước khi xóa.
    """
    # Tái sử dụng service get_by_id để kiểm tra blog tồn tại
    blog_to_delete = get_by_id(blog_id, db) 
    
    blog_repository.delete_blog(blog_to_delete, db)
    return # Không cần trả về gì cả

def update(blog_id: int, blog_dto: dto.BlogCreateRequest, db: Session) -> models.Blog:
    """
    Service để cập nhật 1 blog.
    Chứa logic kiểm tra tồn tại và logic cập nhật.
    """
    # Tái sử dụng service get_by_id để kiểm tra blog tồn tại
    blog_to_update = get_by_id(blog_id, db)
    
    # Gọi repo để cập nhật
    return blog_repository.update_blog(blog_to_update, blog_dto, db)