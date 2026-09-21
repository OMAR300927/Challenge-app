import pytest

from fastapi import status


# test user register
@pytest.mark.asyncio
async def test_user_register(register_response):
  response = register_response

  data = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert data['username'] == 'testuser'
  assert data['email'] == 'test@example.com'


# test user login
@pytest.mark.asyncio
async def test_user_login(login_response):
  response = login_response

  data = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert data['username'] == 'testuser'
  assert data['email'] == 'test@example.com'


# test user logout
@pytest.mark.asyncio
async def test_user_logout(login_user):
  response = await login_user.post(
    '/api/users/logout'
  )

  assert response.status_code == status.HTTP_200_OK


# test check current user
@pytest.mark.asyncio
async def test_check_current_user(login_user):
  response = await login_user.get("/api/users/me")

  data = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert data is not None


# test reset user quota
@pytest.mark.asyncio
async def test_reset_user_quota(login_user):
  response = await login_user.post("/api/users/reset-quota")

  assert response.status_code == status.HTTP_200_OK


# test upload file
@pytest.mark.asyncio
async def test_upload_profile_image(login_user, mocker):
  files = {
    "file": ("avatar.jpg", b"fake image data", "image/jpeg")
  }

  mock_imagekit = mocker.patch(
    "src.services.user.imagekit"
  )

  mock_imagekit_result = mocker.Mock()
  mock_imagekit_result.url = (
    "https://fake-image.com/avatar.jpg"
  )

  mock_imagekit.files.upload.return_value = (
    mock_imagekit_result
  )
  
  response = await login_user.post("/api/users/profile/image", files=files)

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == (
    "https://fake-image.com/avatar.jpg"
  )


# test get user profile image
@pytest.mark.asyncio
async def test_get_user_profile_image(login_user):
  response = await login_user.get('/api/users/get-image')

  assert response.status_code == status.HTTP_200_OK


# test get user quota
@pytest.mark.asyncio
async def test_get_user_quota(login_user):
  response = await login_user.get('/api/users/get-quota')

  assert response.status_code == status.HTTP_200_OK


# test get username
@pytest.mark.asyncio
async def test_get_username(login_user):
  response = await login_user.get('/api/users/username')

  assert response.status_code == status.HTTP_200_OK


# test change user username
@pytest.mark.asyncio
async def test_change_username(login_user):
  newUsername = 'NewUsername123'

  response = await login_user.post(
    '/api/users/change-username',
    json={"username": newUsername}
  )

  assert response.status_code == status.HTTP_200_OK
