from google.genai import Client, types

from .config import settings
from ..schemas.challenge import ChallengeCreate
from .prompts import Prompt

client = Client(api_key=settings.google_api_key.get_secret_value())

async def generate_challenge() -> ChallengeCreate:
  response = await client.aio.models.generate_content(
    model="gemini-3-flash-preview",
    contents=Prompt,
    config=types.GenerateContentConfig(
      response_mime_type="application/json",
      response_schema=ChallengeCreate,
    ),
  )
  if not isinstance(response.parsed, ChallengeCreate):
    raise ValueError("Invalid challenge response")

  return response.parsed