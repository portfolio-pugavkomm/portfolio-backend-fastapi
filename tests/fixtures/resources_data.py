import random

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.models import ResourceSkillModel
from src.apps.v1.resources.schemas import AddResourceSkillSchema

fake = Faker()


@pytest.fixture(scope="function")
def add_skill_schema() -> AddResourceSkillSchema:
    return AddResourceSkillSchema(name=fake.text(10), weight=random.randint(-100, 100))


@pytest.fixture(scope="function")
def skill(request: pytest.FixtureRequest) -> ResourceSkillModel:
    if hasattr(request, "param"):
        name: str = getattr(request, "param")
    else:
        name = fake.text(100)
    return ResourceSkillModel(name=name)


@pytest_asyncio.fixture(scope="function")
async def created_skill(db_session: AsyncSession, skill: ResourceSkillModel) -> ResourceSkillModel:
    db_session.add(skill)
    await db_session.commit()
    await db_session.refresh(skill)
    return skill
