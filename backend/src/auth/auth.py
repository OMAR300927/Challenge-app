import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi import Request

from ..core.config import settings


pass_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
  return pass_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
  return pass_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
  to_encode = data.copy()
  if expires_delta is None:
    expires_delta = timedelta(
      minutes=settings.expire_token_minutes
    )

  expire = datetime.now(timezone.utc) + expires_delta

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(
    to_encode,
    settings.secret_key.get_secret_value(),
    algorithm=settings.algorithm
  )
  return encoded_jwt


def verify_access_token(token: str) -> dict | None:
  try:
    payload = jwt.decode(
      token,
      settings.secret_key.get_secret_value(),
      algorithms=[settings.algorithm]
    )
    return payload
  
  except jwt.ExpiredSignatureError:
    return None
  
  except jwt.InvalidTokenError:
    return None


def get_current_user(request: Request) -> str | None:
  token = request.cookies.get("access_token")
  if not token:
    return None
  
  payload = verify_access_token(token) 
  if not payload:
    return None

  user_id = payload.get("sub")
  if not user_id:
    return None
  
  return str(user_id)