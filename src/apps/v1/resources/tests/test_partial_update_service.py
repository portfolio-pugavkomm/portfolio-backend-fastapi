import pytest
from faker import Faker
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.schemas import ResourceSkillPartialSchema
from src.apps.v1.resources.services import PartialUpdateSkillService

fake = Faker()


@pytest.mark.asyncio
async def test_should_raise_404(db_session: AsyncSession) -> None:
    data = ResourceSkillPartialSchema(name=fake.text(100))
    service = PartialUpdateSkillService(-100, data, db_session)
    with pytest.raises(HTTPException, match="404: Skill not found"):
        await service.execute()
