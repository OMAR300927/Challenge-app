from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
  username: str = Field(min_length=3, max_length=50, description="User's username")
  email: EmailStr = Field(min_length=3, description="User's email address")
  password: str = Field(min_length=8, description="User's password")


class UserLogin(BaseModel):
  email: EmailStr = Field(min_length=3, description="User's email address")
  password: str = Field(min_length=8, description="User's password")


class UserResponse(BaseModel):
  model_config = ConfigDict(
    from_attributes=True
  )

  id: UUID
  username: str
  email: EmailStr
  image_url: str | None = None
  quota: int
  quota_remaining: int
  quota_reset_at: datetime

