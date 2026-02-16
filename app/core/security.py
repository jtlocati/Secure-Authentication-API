from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

#Handels password hashing and JWT token creation/verification.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Hashes the password using bcrypt.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#verifies that the OG  password is equal to hashed version
#Returns bool dependent on wether the passwords match.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Creates a JWT token with the subject (user ID as str) and role, and an optional expiration time.
def create_access_token(subject: str, role: str, exspires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=exspires_minutes if exspires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MIN
    )
    payload: dict[str, Any] = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

#Decodes the JWT token and returns the payload as a dict.
def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError as e:
        raise ValueError("Invalid token") from e