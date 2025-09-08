import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.models import ResourceSkillModel
from src.apps.v1.resources.services import DeleteSkillService


@pytest.mark.asyncio
async def test_should_delete_skill(created_skill: ResourceSkillModel, db_session: AsyncSession) -> None:
    service = DeleteSkillService(created_skill.id, db_session)
    await service.execute()


@pytest.mark.asyncio
async def test_should_raise_http_exception_because_skill_not_found_with_id(db_session: AsyncSession) -> None:
    service = DeleteSkillService(-100, db_session)
    with pytest.raises(HTTPException, match="404: Skill not found"):
        await service.execute()
