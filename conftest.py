import asyncio
from asyncio import AbstractEventLoop
from enum import Enum
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.pool.impl import StaticPool

from src.apps import *  # noqa
from src.config import get_app_settings
from src.database import Base

pytest_plugins = [
    "tests.fixtures.user_data",
    "tests.fixtures.resources_data",
]

settings = get_app_settings()


class PytestOptions(Enum):
    DB_URL = "--dburl"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        PytestOptions.DB_URL.value,
        action="store",
        default=settings.SQLALCHEMY_DATABASE_URL,
    )


@pytest.fixture(scope="session")
def db_url(request: pytest.FixtureRequest) -> str | None:
    return request.config.getoption(PytestOptions.DB_URL.value)


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_url: str) -> AsyncGenerator[AsyncSession, Any]:
    connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}
    engine = create_async_engine(db_url, poolclass=StaticPool, connect_args=connect_args)
    TestSession = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)
    conn = await engine.connect()
    transaction = await conn.begin()
    ses = TestSession(bind=conn)
    try:
        await conn.run_sync(Base.metadata.create_all)
        yield ses
    finally:
        await ses.close()
        await transaction.rollback()
        await conn.close()
        await engine.dispose()


@pytest.fixture(scope="module")
def application() -> FastAPI:
    from src.main import app

    return app
