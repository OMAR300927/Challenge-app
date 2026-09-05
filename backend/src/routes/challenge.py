from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.challenge import ChallengeResponse
from ..database.db import get_db
from ..services.challenge import create_challenge, get_challenges, delete_challenge
from ..auth.auth import get_current_user

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post('/create', response_model=ChallengeResponse)
async def create_new_challenge(db: db_dependency, current_user = Depends(get_current_user)):
  return await create_challenge(db, current_user)

@router.get('/all-challenges', response_model=list[ChallengeResponse])
async def get_all_challenges(db: db_dependency, current_user = Depends(get_current_user)):
  return await get_challenges(db, current_user)

@router.delete('/delete/{challenge_id}')
async def delete_existing_challenge(challenge_id: UUID, db: db_dependency, current_user = Depends(get_current_user)):
  return await delete_challenge(db, challenge_id, current_user)