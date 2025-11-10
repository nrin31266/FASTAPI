from sqlalchemy.orm import Session
from src import models
from sqlalchemy import text

def insert_if_not_exists(
    db: Session, order_id: int, product_id: str, quantity: int
) -> None:
    qr = """
    INSERT INTO reserved_orders (order_id, product_id, quantity)
    VALUES (:order_id, :product_id, :quantity)
    ON CONFLICT (order_id, product_id) DO NOTHING
    """
    result = db.execute(
        text(qr), {"order_id": order_id, "product_id": product_id, "quantity": quantity}
    )
    db.commit()


def delete_reserved_order(db: Session, order_id: int, product_id: str) -> None:
    qr = """
    DELETE FROM reserved_orders
    WHERE order_id = :order_id AND product_id = :product_id
    """
    db.execute(text(qr), {"order_id": order_id, "product_id": product_id})
    db.commit()


def get_by_order_id_and_product_id(
    db: Session, order_id: int, product_id: str
) -> models.ReservedOrder | None:
    return (
        db.query(models.ReservedOrder)
        .filter(
            models.ReservedOrder.order_id == order_id,
            models.ReservedOrder.product_id == product_id,
        )
        .first()
    )
