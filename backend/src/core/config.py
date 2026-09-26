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
    test_database_url: str

    secret_key: SecretStr
    algorithm: str = "HS256"
    expire_token_minutes: int = 30

    google_api_key: SecretStr

    imagekit_private_key: SecretStr

    rabbitmq_user: str
    rabbitmq_pass: str
    broker_url: str

    mailtrap_host: str
    mailtrap_port: int
    mailtrap_username: str
    mailtrap_password: str
    mailtrap_from_email: str
    mailtrap_from_name: str
    mailtrap_to_email: str

    postgres_db: str
    postgres_user: str
    postgres_pass: str



settings = Settings() #type: ignore