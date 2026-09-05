from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
    )

    database_url: str
    allow_origins: str
    api_prefix: str

    secret_key: SecretStr
    algorithm: str = "HS256"
    expire_token_minutes: int = 30

    google_api_key: SecretStr

    imagekit_private_key: SecretStr



settings = Settings() #type: ignore