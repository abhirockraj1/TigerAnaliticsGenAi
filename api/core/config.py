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