from typing import Annotated
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user import UserRegister, UserLogin
from ..database.db import get_db
from ..services.user import user_register, user_login, user_logout
from ..auth.auth import get_current_user

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post('/register')
async def register_user(user: UserRegister, db: db_dependency):
  return await user_register(db, user)

@router.post('/login')
async def login_user(user: UserLogin, db: db_dependency, response: Response):
  return await user_login(db, user, response)

@router.post('/logout')
async def logout_user(response: Response):
  return await user_logout(response)

@router.get('/me')
async def profile(current_user = Depends(get_current_user)):
  return current_user