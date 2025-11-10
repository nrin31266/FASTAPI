from sqlalchemy.orm import Session
from src import models
from sqlalchemy import text

def get_all_products(db: Session):
    return db.query(models.Product).all()


def get_product_by_id(product_id: int, db: Session):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(product: models.Product, db: Session):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def decrease_stock_if_available(product_id: str, quantity: int, db: Session) -> bool:
    qr = """
              UPDATE products SET quantity = quantity - :quantity, updated_at = CURRENT_TIMESTAMP
              WHERE product_id = :product_id AND quantity >= :quantity
              """
    result = db.execute(text(qr), {"quantity": quantity, "product_id": product_id})
    db.commit()
    return result.rowcount > 0


def increase_stock(db: Session, product_id: str, quantity: int, ) -> None:
    qr = """
          UPDATE products SET quantity = quantity + :quantity, updated_at = CURRENT_TIMESTAMP
          WHERE product_id = :product_id
          """
    db.execute(text(qr), {"quantity": quantity, "product_id": product_id})
    db.commit()
