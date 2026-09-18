import pytest
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  AsyncSession,
  async_sessionmaker
)
from sqlalchemy.pool import NullPool

from ..database.db import Base, get_db
from ..main import app
from ..core.config import settings
from ..models.model import User, Challenge
from ..auth.auth import hash_password



@pytest.fixture(scope='session')
async def test_engine():
  engine = create_async_engine(
    settings.test_database_url,
    poolclass=NullPool
  )

  yield engine

  await engine.dispose()

@pytest.fixture(scope='session')
async def test_database(test_engine):
  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  yield

  async with test_engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(
  test_engine,
  test_database
) -> AsyncGenerator[AsyncSession, None]:
  conn = await test_engine.connect()
  tran = await conn.begin()

  Local_session = async_sessionmaker(
    bind=conn,
    class_=AsyncSession,
    expire_on_commit=False,
    join_transaction_mode="create_savepoint"
  )

  async with Local_session() as session:
    try:
      yield session

    finally:
      await session.close()
      await tran.rollback()
      await conn.close()

@pytest.fixture
async def client(
  db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
  async def override_db():
    yield db_session

  app.dependency_overrides[get_db] = override_db

  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url='http://test'
  ) as ac:
    yield ac

  app.dependency_overrides.clear()

@pytest.fixture
async def register_user(client):
    response = await client.post(
      "/api/users/register",
      json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123"
      },
    )

    assert response.status_code == 201

    return {
      "email": "test@example.com",
      "password": "TestPassword123"
    }

@pytest.fixture
async def login_user(client, register_user):
    response = await client.post(
      "/api/users/login",
      json=register_user
    )

    assert response.status_code == 201

    return client

@pytest.fixture
async def user(db_session):
  user = User(
    username="testuser1",
    email="test1@example.com",
    password=hash_password("test_hash_password1")
  )

  db_session.add(user)
  await db_session.flush()

  return user

@pytest.fixture
async def user_challenge(db_session, user):
  challenge = Challenge(
    user_id=user.id,
    question='This is a testing question?',
    options=['1', '2', '3', '4'],
    correct_answer='1',
    explanation='This is explaining for the testing question'
  )

  db_session.add(challenge)
  await db_session.flush()

  return challenge