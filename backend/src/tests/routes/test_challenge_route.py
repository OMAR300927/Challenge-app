from types import SimpleNamespace

import pytest
from unittest.mock import AsyncMock

from fastapi import status
from sqlalchemy import select

from ...models.model import User, Challenge


# test create challenge
@pytest.mark.asyncio
async def test_create_challenge(login_user, mocker):
  generated_challenge = SimpleNamespace(
    question="What is Python?",
    options=["A", "B", "C", "D"],
    correct_answer="A",
    explanation="Python is a programming language."
  )

  mocker.patch(
    "src.services.challenge.generate_challenge",
    new_callable=AsyncMock,
    return_value=generated_challenge
  )

  mocker.patch(
    "src.services.challenge.send_challenge_create_message"
  )

  response = await login_user.post(
    '/api/challenges/create'
  )

  assert response.status_code == status.HTTP_200_OK


# test get all challenges
async def test_get_all_challenges(login_user):
  response = await login_user.get("/api/challenges/all-challenges")

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json()["detail"] == "No challenges found for this user"


# test delete challenge
@pytest.mark.asyncio
async def test_delete_challenge(login_user, db_session, register_user):
  result = await db_session.execute(
    select(User).where(User.email == register_user["email"])
  )
  user = result.scalar_one()

  challenge = Challenge(
    user_id=user.id,
    question="This is a test question?",
    options=["1", "2", "3", "4"],
    correct_answer="1",
    explanation="Test explanation"
  )

  db_session.add(challenge)
  await db_session.flush()

  response = await login_user.delete(
    f"/api/challenges/delete/{challenge.id}"
  )

  assert response.status_code == status.HTTP_200_OK