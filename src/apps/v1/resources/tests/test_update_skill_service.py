import pytest
from faker import Faker
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.models import ResourceSkillModel
from src.apps.v1.resources.schemas import AddResourceSkillSchema, ResourceSkillSchema
from src.apps.v1.resources.services import UpdateSkillService

fake = Faker()


@pytest.mark.asyncio
async def test_should_raise_http_exception_404(
    db_session: AsyncSession,
    add_skill_schema: AddResourceSkillSchema,
) -> None:
    service = UpdateSkillService(-100, add_skill_schema, db_session)

    with pytest.raises(HTTPException, match="404: Skill not found"):
        await service.execute()


@pytest.mark.asyncio
async def test_should_update_skill(
    add_skill_schema: AddResourceSkillSchema,
    db_session: AsyncSession,
    created_skill: ResourceSkillModel,
) -> None:
    service = UpdateSkillService(created_skill.id, add_skill_schema, db_session)
    response = await service.execute()

    await db_session.refresh(created_skill)

    assert isinstance(response, ResourceSkillSchema)
    assert response.name == add_skill_schema.name
    assert response.weight == add_skill_schema.weight

    assert created_skill.name == add_skill_schema.name
    assert created_skill.weight == add_skill_schema.weight
