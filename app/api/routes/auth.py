from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.schemas.user import UserOut
from app.services.users import get_user_by_email, create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def login(data: LoginIn, db: Session = Depends(get_db)):
    
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalad email or password")
    
    token = create_access_token(subject=str(user.id), role=user.role)

    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user