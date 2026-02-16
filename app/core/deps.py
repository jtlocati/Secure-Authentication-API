from collections.abc import Generator
from app.db.session import SessionLocal

#Provides route a safe DB session per request.
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import decode_token
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=True)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:

    token = creds.credentials

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalad or expired token")
    
    sub = payload.get("sub")

    if sub == None:
        raise HTTPException(status_code=401, detail="Invalad token payload")
    
    user = db.scalar(select(User).where(User.id == int(sub)))

    if user == None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
