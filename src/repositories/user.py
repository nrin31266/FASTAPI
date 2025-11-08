from sqlalchemy.orm import Session
from src import models, dto


def create(db: Session, user: models.User) -> models.User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()
    