from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..core.config import settings


engine = create_async_engine(
  settings.database_url
)

SessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False
)

class Base(DeclarativeBase):
  pass

async def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    await db.close()

async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)