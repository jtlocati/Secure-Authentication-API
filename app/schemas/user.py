from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
