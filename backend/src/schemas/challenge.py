from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ChallengeCreate(BaseModel):
  question: str = Field(min_length=1, max_length=255, description="Challenge question")
  options: list[str] = Field(description="List of challenge options")
  correct_answer: str = Field(min_length=1, max_length=255, description="Correct answer for the challenge")
  explanation: str = Field(max_length=1000, description="Explanation for the correct answer")


class ChallengeResponse(BaseModel):
  model_config = ConfigDict(
    from_attributes=True
  )

  id: UUID
  user_id: UUID
  question: str
  options: list[str]
  correct_answer: str
  explanation: str | None = None