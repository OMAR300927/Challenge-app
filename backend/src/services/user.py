from typing import Annotated
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ..models.model import User
from ..auth.auth import hash_password, verify_password, create_access_token
from ..database.db import get_db
from ..schemas.user import UserRegister, UserLogin
from ..utils.imagekit import imagekit

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

async def reset_quota_time(db: db_dependency, user_id: UUID):
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

async def image_profile(db: db_dependency, user_id: UUID, file: UploadFile):
  get_user = await db.execute(select(User).where(User.id == user_id))
  user = get_user.scalar_one_or_none()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found",
    )

  if not file.filename:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="File name is required",
    )

  image_data = await file.read()

  upload_image = imagekit.files.upload(
    file=image_data,
    file_name=file.filename
  )

  user.image_url = upload_image.url
  await db.commit()
  await db.refresh(user)
  return user.image_url

async def get_profile_image(db: db_dependency, user_id: UUID):
  get_image = await db.execute(select(User.image_url).where(User.id == user_id))
  result = get_image.scalar_one_or_none()

  return result

async def get_quotas(db: db_dependency, user_id: UUID):
  quota = await db.execute(select(User.quota_remaining, User.quota_reset_at).where(User.id == user_id))
  result = quota.one_or_none()

  if not result:
    return None

  return {
    "quota": result.quota_remaining,
    "quota_reset_at": result.quota_reset_at
  }

async def get_user_by_username(db: db_dependency, user_id: UUID):
  username = await db.execute(select(User.username).where(User.id == user_id))
  result = username.scalar_one_or_none()

  return result

async def update_username(db: db_dependency, user_id: UUID, username: str):
  get_username = await db.execute(select(User.username).where(User.id == user_id))
  result = get_username.scalar_one_or_none()

  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User does not exist'
    )

  await db.execute(
    update(User).where(User.id == user_id).values(username=username)
  )
  await db.commit()
  return username