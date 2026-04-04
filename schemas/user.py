from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Column, DateTime

created_at = Column(DateTime, default=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)