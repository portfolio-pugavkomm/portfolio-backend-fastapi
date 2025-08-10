from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import get_app_settings

settings = get_app_settings()

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
session = async_sessionmaker(engine, expire_on_commit=settings.SQLALCHEMY_EXPIRE_ON_COMMIT)


class Base(DeclarativeBase):
    pass


async def get_db_ses() -> AsyncGenerator[AsyncSession, Any]:
    async with session() as ses:
        yield ses
