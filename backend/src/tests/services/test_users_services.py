from datetime import datetime, timedelta, timezone
from uuid import uuid4
from io import BytesIO

import pytest
from fastapi import HTTPException, Response, status, UploadFile
from sqlalchemy import select

from ...models.model import User
from ...services.user import (
  get_user_by_email,
  user_register,
  user_login,
  user_logout,
  reset_quota_time,
  image_profile,
  get_profile_image,
  get_quotas,
  get_user_by_username,
  update_username
)
from ...auth.auth import verify_password, hash_password
from ...schemas.user import UserRegister, UserLogin


# test get user email function
@pytest.mark.asyncio
async def test_get_user_by_email(db_session, user):
  result = await get_user_by_email(
    db_session,
    user.email
  )

  assert result is not None
  assert result.email == 'test1@example.com'



# test user register function
@pytest.mark.asyncio
async def test_user_register(db_session):
  user = UserRegister(
    username='testuser1',
    email='test1@example.com',
    password='test_hash_password1'
  )

  result = await user_register(db_session, user)

  assert result is not None
  assert result.username == 'testuser1'
  assert result.email == 'test1@example.com'
  assert verify_password('test_hash_password1', result.password)

@pytest.mark.asyncio
async def test_user_email_existing(db_session, user):
  duplicate_user = UserRegister(
    username="testuser2",
    email=user.email,
    password="test_hash_password2"
  )

  with pytest.raises(HTTPException) as e:
    await user_register(db_session, duplicate_user)

  assert e.value.status_code == status.HTTP_400_BAD_REQUEST
  assert e.value.detail == "Email already registered"



# test user login function
@pytest.mark.asyncio
async def test_user_login(db_session):
  response = Response()

  register_user = UserRegister(
    username='testuser1',
    email='test1@example.com',
    password='test_hash_password1'
  )

  register_result = await user_register(db_session, register_user)

  assert register_result is not None

  login_user = UserLogin(
    email=register_user.email,
    password=register_user.password
  )

  login_result = await user_login(db_session, login_user, response)

  assert login_result is not None
  assert "access_token" in response.headers['set-cookie']
  assert login_result.email == register_user.email
  assert login_result.username == register_user.username

@pytest.mark.asyncio
async def test_user_email_not_exist(db_session):
  response = Response()

  register_user = UserRegister(
    username='testuser1',
    email='test1@example.com',
    password='test_hash_password1'
  )

  register_result = await user_register(db_session, register_user)

  assert register_result is not None

  login_user = UserLogin(
    email="notexist@example.com",
    password=register_user.password
  )

  with pytest.raises(HTTPException) as e:
    await user_login(db_session, login_user, response)

  assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
  assert e.value.detail == "Invalid email or password"

@pytest.mark.asyncio
async def test_user_password_not_exist(db_session):
  response = Response()

  register_user = UserRegister(
    username='testuser1',
    email='test1@example.com',
    password='test_hash_password1'
  )

  register_result = await user_register(db_session, register_user)

  assert register_result is not None

  login_user = UserLogin(
    email=register_user.email,
    password='test_hash_password2'
  )

  with pytest.raises(HTTPException) as e:
    await user_login(db_session, login_user, response)

  assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
  assert e.value.detail == "Invalid email or password"



#test user logout function
@pytest.mark.asyncio
async def test_user_logout():
  response = Response()

  logout_user = await user_logout(response)

  assert logout_user == {"message": "Logout successful"}
  assert "access_token=" in response.headers["set-cookie"]
  assert "Max-Age=0" in response.headers["set-cookie"]



# test reset quota for the user function
@pytest.mark.asyncio
async def test_reset_quota_needed(db_session):
  before_time = datetime.now(timezone.utc)

  user = User(
    username="testuser1",
    email="test1@example.com",
    password=hash_password("test_hash_password1"),
    quota_remaining=2,
    quota_reset_at=before_time - timedelta(days=1)
  )

  db_session.add(user)
  await db_session.flush()

  assert user is not None

  await reset_quota_time(db_session, user.id)

  after_time = datetime.now(timezone.utc)

  assert user.quota_remaining == 3
  assert before_time - timedelta(days=1) <= user.quota_reset_at <= after_time + timedelta(days=1)

@pytest.mark.asyncio
async def test_user_not_exist(db_session):
  fake_user_id = uuid4()

  with pytest.raises(HTTPException) as e:
    await reset_quota_time(db_session, fake_user_id)

  assert e.value.status_code == status.HTTP_404_NOT_FOUND
  assert e.value.detail == "User not found"



# test upload user image file function
@pytest.mark.asyncio
async def test_upload_user_image(db_session, user, mocker):
  file = UploadFile(
    filename="avatar.jpg",
    file=BytesIO(b"fake image data")
  )

  mock_imagekit = mocker.patch(
    'src.services.user.imagekit'
  )

  mock_imagekit_result = mocker.Mock()
  mock_imagekit_result.url = "https://fake-image.com/avatar.jpg"

  mock_imagekit.files.upload.return_value = mock_imagekit_result

  result = await image_profile(db_session, user.id, file)

  assert result == "https://fake-image.com/avatar.jpg"
  assert user.image_url == "https://fake-image.com/avatar.jpg"

@pytest.mark.asyncio
async def test_user_not_exist_in_image_profile_function(db_session):
  fake_user_id = uuid4()
  file = UploadFile(
    filename="",
    file=BytesIO(b"fake image data")
  )

  with pytest.raises(HTTPException) as e:
    await image_profile(db_session, fake_user_id, file)

  assert e.value.status_code == status.HTTP_404_NOT_FOUND
  assert e.value.detail == "User not found"

@pytest.mark.asyncio
async def test_upload_user_image_no_filename(db_session, user):
  file = UploadFile(
    filename="",
    file=BytesIO(b"fake image data")
  )

  with pytest.raises(HTTPException) as e:
    await image_profile(db_session, user.id, file)

  assert e.value.status_code == status.HTTP_400_BAD_REQUEST
  assert e.value.detail == "File name is required"



# test getting the profile image function
@pytest.mark.asyncio
async def test_get_user_profile_image(db_session, user):
  user.image_url = "https://fake-image.com/avatar.jpg"

  db_session.add(user)
  await db_session.flush()

  result = await get_profile_image(db_session, user.id)

  assert result == user.image_url



# test getting user quotas function
@pytest.mark.asyncio
async def test_get_user_quotas(db_session, user):
  result = await get_quotas(db_session, user.id)

  assert result is not None
  assert result["quota"] == user.quota_remaining
  assert result["quota_reset_at"] == user.quota_reset_at

@pytest.mark.asyncio
async def test_get_quotas_error(db_session):
  fake_user_id = uuid4()

  result = await get_quotas(db_session, fake_user_id)

  assert result is None



# test get the user username function
@pytest.mark.asyncio
async def test_get_user_by_username(db_session, user):
  result = await get_user_by_username(db_session, user.id)

  assert result is not None
  assert result == 'testuser1'



# test update username function
@pytest.mark.asyncio
async def test_update_the_username(db_session, user):
  result = await update_username(db_session, user.id, 'newUsername')

  updated_username_result = await db_session.execute(
    select(User.username).where(User.id == user.id)
  )

  updated_username = updated_username_result.scalar_one_or_none()

  assert result == 'newUsername'
  assert updated_username == 'newUsername'

@pytest.mark.asyncio
async def test_user_not_exist_in_update_username_function(db_session):
  fake_user_id = uuid4()

  with pytest.raises(HTTPException) as e:
    await update_username(db_session, fake_user_id, 'fakeUsername')

  assert e.value.status_code == status.HTTP_404_NOT_FOUND
  assert e.value.detail == "User does not exist"

@pytest.mark.asyncio
async def test_user_not_updated(db_session, user):
  user2 = User(
    username="testuser2",
    email="test2@example.com",
    password=hash_password("test_hash_password2")
  )

  db_session.add(user2)
  await db_session.flush()

  with pytest.raises(HTTPException) as e:
    await update_username(db_session, user2.id, user.username)

  assert e.value.status_code == status.HTTP_409_CONFLICT
  assert e.value.detail == 'Username already exists'

  import inspect

  print(inspect.getsourcefile(update_username))
  print(inspect.getsourcelines(update_username)[1])