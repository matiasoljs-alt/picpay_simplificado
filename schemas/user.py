from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CreateUser(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=100, unique=True)
    password: str = Field(min_length=8, max_length=100)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    account_balance: float
    role: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(min_length=5, max_length=100, unique=True)
    password: Optional[str] = Field(min_length=8, max_length=100)

