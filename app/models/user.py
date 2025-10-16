# app/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr  
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True