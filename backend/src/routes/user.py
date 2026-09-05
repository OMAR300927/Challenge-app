from typing import Annotated
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user import UserRegister, UserLogin, UserResponse
from ..database.db import get_db
from ..services.user import user_register, user_login, user_logout
from ..services.challenge import reset_quota_time
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