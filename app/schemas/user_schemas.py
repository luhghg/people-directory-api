from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
