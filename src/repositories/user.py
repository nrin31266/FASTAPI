from sqlalchemy.orm import Session
from src import models, dto


def create(db: Session, user: models.User) -> models.User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_keycloak_id(db: Session, keycloak_id: str) -> models.User | None:
    return db.query(models.User).filter(models.User.keycloak_id == keycloak_id).first()

def get_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()