import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PG_HOST: str
    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: str
    PG_SCHEMA: str
    PG_PORT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
