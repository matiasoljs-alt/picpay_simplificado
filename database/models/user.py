from sqlmodel import SQLModel, Session, Field
from typing import Optional
from pydantic import EmailStr

class Userdb(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=100, unique=True)
    hashed_password: str = Field(min_length=8, max_length=100)
    account_balance: float = Field(default=0.0, ge=0.0)
    role: str = Field(default="user", max_length=20)

