from collections.abc import Generator
from app.db.session import SessionLocal

#Provides route a safe DB session per request.
def get_db() -> Generator:
    db = SessionLocal()
    try:
        #allows fastAPI to inject current session into route functions
        yield db
    #garuntees route even if error is thrown
    finally:
        db.close()

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import decode_token
from app.models.user import User

#Reads authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=True)

#pulls token string from header
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:

    token = creds.credentials

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalad or expired token")
    
    #pulls user id
    sub = payload.get("sub")

    #Querys DB for user.id == sub
    if sub == None:
        raise HTTPException(status_code=401, detail="Invalad token payload")
    
    user = db.scalar(select(User).where(User.id == int(sub)))

    if user == None:
        raise HTTPException(status_code=401, detail="User not found")
    
    #Return user object if exsists, else return 401
    return user
