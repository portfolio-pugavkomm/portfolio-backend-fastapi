import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRES: int = int(os.getenv("JWT_ACCESS_EXPIRES", 60))
    JWT_REFRESH_EXPIRES: int = int(os.getenv("JWT_REFRESH_EXPIRES", 600))
    ROTATE_REFRESH: bool = os.getenv("ROTATE_REFRESH") == 1


@lru_cache
def get_config() -> AuthConfig:
    _SECRET_KEY = os.getenv("SECRET_KEY")
    if _SECRET_KEY is None:
        raise ValueError("Required secret key")
    return AuthConfig(SECRET_KEY=_SECRET_KEY)
