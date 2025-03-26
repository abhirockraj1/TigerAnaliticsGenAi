# app/api/core/config.py
from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/mydb"
    secret_key: str = secrets.token_hex(32)
    access_token_expire_minutes: int = 30
    OPENROUTER_API_KEY: str = "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"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()