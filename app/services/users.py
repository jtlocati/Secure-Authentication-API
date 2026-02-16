from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.core.security import verify_password, hash_password

#Models for DB structure

#lookup user baised on email
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

#Creates new user
def create_user(db: Session, email: str, password: str, role: str = "user") -> User:
    #New user with hashed pass, email, and role
    user = User(email=email, hashed_password=hash_password(password), role=role)
    #adds new user row
    db.add(user)
    #commits info to DB
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    #Fetches user by email
    user = get_user_by_email(db, email)
    if not user:
        return None
    #calls back to security and verifys if entered pass == hashed_password
    if not verify_password(password, user.hashed_password):
        return None
    return user
