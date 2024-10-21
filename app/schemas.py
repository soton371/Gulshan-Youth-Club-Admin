from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


# for admin
class AdminOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
        
        
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

