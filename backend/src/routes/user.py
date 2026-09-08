from typing import Annotated
from fastapi import APIRouter, Depends, Response, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user import UserRegister, UserLogin, UserResponse
from ..database.db import get_db
from ..services.user import user_register, user_login, user_logout, image_profile, reset_quota_time, get_profile_image, get_quotas
from ..auth.auth import get_current_user

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post('/register', response_model=UserResponse)
async def register_user(user: UserRegister, db: db_dependency):
  return await user_register(db, user)

@router.post('/login', response_model=UserResponse)
async def login_user(user: UserLogin, db: db_dependency, response: Response):
  return await user_login(db, user, response)

@router.post('/logout')
async def logout_user(response: Response):
  return await user_logout(response)

@router.get('/me')
async def check_the_current_user(current_user = Depends(get_current_user)):
  return current_user

@router.post('/reset-quota')
async def reset_user_quota(db: db_dependency, current_user = Depends(get_current_user)):
  return await reset_quota_time(db, current_user.id)

@router.post('/profile/image', response_model=UserResponse)
async def upload_profile_image(
  db: db_dependency,
  current_user = Depends(get_current_user),
  file: UploadFile = File(...)
  ):
  return await image_profile(db, current_user, file)

@router.get('/get-image')
async def profile_image(
  db: db_dependency,
  current_user = Depends(get_current_user)
):
  return await get_profile_image(db, current_user)

@router.get('/get-quota')
async def get_user_quotas(db: db_dependency, current_user = Depends(get_current_user)):
  return await get_quotas(db, current_user)