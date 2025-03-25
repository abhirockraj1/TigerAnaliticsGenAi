# app/api/core/config.py
from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/mydb"
    secret_key: str = secrets.token_hex(32)
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()