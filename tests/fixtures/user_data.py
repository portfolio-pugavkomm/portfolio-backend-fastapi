from typing import AsyncGenerator

import faker
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.utils import get_user_model_util

fake = faker.Faker()

User = get_user_model_util()


@pytest.fixture(scope="function")
def new_user():  # type: ignore
    return User(username=fake.user_name())


@pytest.fixture(scope="function")
async def created_user(db_session: AsyncSession, new_user: User) -> AsyncGenerator[User, None]:  # type: ignore
    db_session.add(new_user)
    await db_session.connection()
    await db_session.refresh(new_user)
    yield new_user
