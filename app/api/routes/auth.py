from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.schemas.user import UserOut
from app.services.users import get_user_by_email, create_user, authenticate_user
from app.core.security import create_access_token
from app.core.deps import require_role

#Groups endpoints under "auth"
router = APIRouter(prefix="/auth", tags=["auth"])

#Checks if email alredy exsists, creates user if not, returns safe user info
#checks valid email/pass, issues JWT if correct
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    
    #finds exsisting user of the email inputed, if found a 400 is thrown
    existing = get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email Already Registered")
    
    user = create_user(db, data.email, data.password)
    return user


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    #returns a object "user" dependent of where there is a matchin email
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(subject=str(user.id), role=user.role)

    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def admin_only(_admin=Depends(require_role("admin"))):
    return {"ok": True, "message": "You are an admin"}
