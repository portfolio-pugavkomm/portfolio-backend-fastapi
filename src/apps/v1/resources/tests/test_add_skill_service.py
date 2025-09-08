import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.schemas import AddResourceSkillSchema, ResourceSkillSchema
from src.apps.v1.resources.services import AddSkillService

fake = Faker()


@pytest.mark.asyncio
async def test_should_create_skill(db_session: AsyncSession, add_skill_schema: AddResourceSkillSchema) -> None:
    service = AddSkillService(add_skill_schema, db_session)

    response = await service.execute()

    assert isinstance(response, ResourceSkillSchema)
    assert response.name == add_skill_schema.name
    assert response.weight == add_skill_schema.weight
