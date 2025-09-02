from typing import AsyncGenerator

import faker
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.utils import get_user_model_util

fake = faker.Faker()

User = get_user_model_util()


@pytest.fixture(scope="function")
def new_user():  # type: ignore
    return User(username=fake.user_name(), password=fake.password())


@pytest_asyncio.fixture(scope="function")
async def created_user(db_session: AsyncSession, new_user: User) -> AsyncGenerator[User, None]:  # type: ignore
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    yield new_user
