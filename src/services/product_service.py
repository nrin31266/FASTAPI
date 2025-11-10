from sqlalchemy.orm import Session
from src import dto, models
from src.repositories import product_repository
from src.errors.base_exception import BaseException
from src.errors.base_error_code import BaseErrorCode


def get_all_products(db: Session) -> list[dto.ProductResponse]:
    products = product_repository.get_all_products(db)
    return [dto.ProductResponse.model_validate(product) for product in products]


def get_product_by_id(product_id: int, db: Session) -> dto.ProductResponse:
    product = product_repository.get_product_by_id(product_id, db)
    if not product:
        raise BaseException(
            BaseErrorCode.NOT_FOUND, f"Product with id {product_id} not found"
        )
    return dto.ProductResponse.model_validate(product)


def create_product(
    product_dto: dto.ProductCreationRequest, db: Session
) -> dto.ProductResponse:
    new_product = models.Product(
        product_id=product_dto.product_id, price=product_dto.price, quantity=product_dto.quantity
    )
    created_product = product_repository.create_product(new_product, db)
    return dto.ProductResponse.model_validate(created_product)
