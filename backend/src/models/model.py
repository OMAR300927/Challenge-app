from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from sqlalchemy import JSON, func, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    image_url: Mapped[str] = mapped_column(nullable=True)
    quota: Mapped[int] = mapped_column(default=3)
    quota_remaining: Mapped[int] = mapped_column(default=3)
    quota_reset_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1)
    )

    challenges = relationship("Challenge", back_populates="user")


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    question: Mapped[str] = mapped_column(nullable=False)
    options: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    correct_answer: Mapped[str] = mapped_column(nullable=False)
    explanation: Mapped[str] = mapped_column(nullable=True)

    user = relationship("User", back_populates="challenges")