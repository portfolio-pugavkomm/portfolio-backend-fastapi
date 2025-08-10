import os
from pathlib import Path, PurePath

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

INSTALLED_APPS = [
    "src.apps.v1.auth",
]


class BaseAppConfig(BaseSettings):
    API_NAME: str = "Portfolio Mechislav P."
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///dev.db")
    SQLALCHEMY_EXPIRE_ON_COMMIT: bool = bool(os.getenv("SQLALCHEMY_EXPIRE_ON_COMMIT", False))
    BASE_DIR: PurePath = BASE_DIR
    MODEL_FILE_NAME: str = "models.py"
    INSTALLED_APPS: list[str] = INSTALLED_APPS


def get_app_settings() -> BaseAppConfig:
    return BaseAppConfig()
