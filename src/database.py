import datetime
import uuid
from typing import Annotated, Any, AsyncGenerator
from uuid import UUID

from sqlalchemy import BIGINT, TIMESTAMP, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from src.config import get_app_settings

settings = get_app_settings()

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
session = async_sessionmaker(engine, expire_on_commit=settings.SQLALCHEMY_EXPIRE_ON_COMMIT)

str_256 = Annotated[str, 256]
pk_int = Annotated[int, mapped_column(primary_key=True)]
pk_uuid = Annotated[UUID, mapped_column(primary_key=True, default=uuid.uuid4)]


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BIGINT,
        datetime.datetime: TIMESTAMP(timezone=True),
        str_256: String(256),
    }


async def get_db_ses() -> AsyncGenerator[AsyncSession, Any]:
    async with session() as ses:
        yield ses
