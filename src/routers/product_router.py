from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from src import dto
from src.database import get_db
from src.dto import ApiResponse
from src.services import product_service
from src.keycloak_auth.dto import UserPrincipal
from src.keycloak_auth.dependencies import get_current_user, require_roles
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/inventories", tags=["inventories"])


@router.get("", response_model=ApiResponse[List[dto.ProductResponse]])
def get_products(
    db: Session = Depends(get_db),
    current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"])),
):
    products = product_service.get_all_products(db)
    return ApiResponse.success(data=products)

@router.get("/1", response_model=ApiResponse[List[dto.ProductResponse]])
def get_products(
    db: Session = Depends(get_db),
    # current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"])),
):
    products = product_service.get_all_products(db)
    return ApiResponse.success(data=products)


@router.post(
    "",
    response_model=ApiResponse[dto.ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: dto.ProductCreationRequest,
    db: Session = Depends(get_db),
    current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"])),
):
    new_product = product_service.create_product(product, db)
    logger.info(f"User {current_user.email} created a new product: {new_product.product_id}")
    return ApiResponse.success(data=new_product, message="Product created successfully")


@router.get("/{id}", response_model=ApiResponse[dto.ProductResponse])
def get_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserPrincipal = Depends(get_current_user),
):
    product = product_service.get_product_by_id(id, db)
    logger.info(f"User {current_user.email} accessed product: {product.id}")
    return ApiResponse.success(data=product)
