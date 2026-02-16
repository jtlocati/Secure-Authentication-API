from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.core.security import verify_password, hash_password

#Models for DB structure

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

def create_user(db: Session, email: str, password: str, role: str = "user") -> User:
    user = User(email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
