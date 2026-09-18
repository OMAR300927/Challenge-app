import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select

from ...services.challenge import get_challenges, delete_challenge, create_challenge
from ...models.model import Challenge, User


# test get user challenges function
@pytest.mark.asyncio
async def test_get_user_challenges(db_session, user, user_challenge):
  result = await get_challenges(db_session, user.id)

  assert len(result) == 1
  assert result[0].id == user_challenge.id
  assert result[0].user_id == user.id

@pytest.mark.asyncio
async def test_challenge_not_exist(db_session, user):
  with pytest.raises(HTTPException) as e:
    await get_challenges(db_session, user.id)

  assert e.value.status_code == status.HTTP_404_NOT_FOUND
  assert e.value.detail == 'No challenges found for this user'



# test delete user challenge
@pytest.mark.asyncio
async def test_delete_user_challenge(db_session, user, user_challenge):
  result = await delete_challenge(db_session, user_challenge.id, user.id)

  assert result == {"message": "Challenge deleted successfully"}

@pytest.mark.asyncio
async def test_challenge_not_found(db_session, user, user_challenge):
  fake_challenge_id = uuid4()

  with pytest.raises(HTTPException) as e:
    await delete_challenge(db_session, fake_challenge_id, user.id)

  assert e.value.status_code == status.HTTP_404_NOT_FOUND
  assert e.value.detail == "Challenge not found"



# test create challenge
@pytest.mark.asyncio
async def test_create_challenge_success(db_session, user, mocker):
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

  result = await create_challenge(
    db_session,
    user.id
  )

  assert result.question == "What is Python?"
  assert result.options == ["A", "B", "C", "D"]
  assert result.correct_answer == "A"
  assert result.explanation == "Python is a programming language."
  assert result.user_id == user.id

  remaining_quota = await db_session.execute(
    select(User.quota_remaining).where(User.id == user.id)
  )

  remaining_quota_result = remaining_quota.scalar_one_or_none()

  assert remaining_quota_result == 2

  saved_challenge = await db_session.execute(
    select(Challenge).where(Challenge.id == result.id)
  )

  saved_challenge_result = saved_challenge.scalar_one_or_none()

  assert saved_challenge_result is not None

@pytest.mark.asyncio
async def test_create_challenge_when_user_has_no_quota(db_session, user):
  user.quota_remaining = 0

  await db_session.flush()

  with pytest.raises(HTTPException) as e:
    await create_challenge(db_session, user.id)

  assert e.value.status_code == status.HTTP_403_FORBIDDEN
  assert e.value.detail == 'Your credits are exhausted. Please wait for the quota to reset.'