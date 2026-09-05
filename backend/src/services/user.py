from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.model import User
from ..auth.auth import hash_password, verify_password, create_access_token
from ..database.db import get_db
from ..schemas.user import UserRegister, UserLogin

db_dependency = Annotated[AsyncSession, Depends(get_db)]

async def get_user_by_email(db: db_dependency, email: str):
  get_user = await db.execute(select(User).where(User.email == email))
  result = get_user.scalar_one_or_none()
  return result

async def user_register(db: db_dependency, user: UserRegister):
  existing_user = await get_user_by_email(db, user.email)
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
  
  new_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(user.password)
  )
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

async def user_login(db: db_dependency, user: UserLogin, response: Response):
  existing_user = await get_user_by_email(db, user.email)
  if not existing_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
  
  if not verify_password(user.password, existing_user.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
  
  token = create_access_token(
    data={"sub": str(existing_user.id)}
  )

  response.set_cookie(
    key="access_token",
    value=token,
    httponly=True
  )

  return existing_user

async def user_logout(response: Response):
  response.delete_cookie(key="access_token")
  return {"message": "Logout successful"}

async def reset_quota_time(db: db_dependency, user_id: str):
  get_user = await db.execute(select(User).where(User.id == user_id))
  user = get_user.scalar_one_or_none()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  
  now = datetime.now(timezone.utc)

  if user.quota_remaining < user.quota and now >= user.quota_reset_at:
    user.quota_remaining = user.quota
    user.quota_reset_at = now + timedelta(days=1)
    await db.commit()
    await db.refresh(user)