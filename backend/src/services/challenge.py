from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.model import Challenge
from ..core.challengeGenerator import generate_challenge
from ..database.db import get_db

db_dependency = Annotated[AsyncSession, Depends(get_db)]

async def create_challenge(db: db_dependency, user_id: UUID) -> Challenge:
  generated_challenge = await generate_challenge()

  new_challenge = Challenge(
    user_id=user_id,
    question=generated_challenge.question,
    options=generated_challenge.options,
    correct_answer=generated_challenge.correct_answer,
    explanation=generated_challenge.explanation
  )
  db.add(new_challenge)
  await db.commit()
  await db.refresh(new_challenge)
  return new_challenge

async def get_challenges(db: db_dependency, user_id: UUID):
  result = await db.execute(select(Challenge).where(Challenge.user_id == user_id))  
  challenges = result.scalars().all()
  if not challenges:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No challenges found for this user")

  return challenges

async def delete_challenge(db: db_dependency, challenge_id: UUID, user_id: UUID):
  result = await db.execute(select(Challenge).where(Challenge.id == challenge_id, Challenge.user_id == user_id))
  challenge = result.scalar_one_or_none()
  if not challenge:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")

  await db.delete(challenge)
  await db.commit()
  return {"message": "Challenge deleted successfully"}