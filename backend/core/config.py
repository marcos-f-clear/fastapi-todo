import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Literal
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
  )

  ENVIRONMENT: Literal['dev', 'pro']

  # Database settings
  DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "postgresql")
  DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
  DATABASE_PORT: int = os.getenv("DATABASE_PORT", 5432)
  DATABASE_USER: str = os.getenv("DATABASE_USER")
  DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
  DATABASE_NAME: str = os.getenv("DATABASE_NAME")

  DATABASE_URL: str = f"{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

  # JWT settings
  SECRET_KEY: str = os.getenv("SECRET_KEY")
  ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days

@lru_cache
def get_settings() -> Settings:
  return Settings()

settings = get_settings()