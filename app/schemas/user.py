from datetime import datetime
from pydantic import BaseModel, EmailStr

#Define user db format:
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
