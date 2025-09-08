from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.models import ResourceSkillModel
from src.apps.v1.resources.schemas import AddResourceSkillSchema, ResourceSkillSchema


class AddSkillService:
    def __init__(self, data: AddResourceSkillSchema, session: AsyncSession) -> None:
        self._data = data
        self._ses = session

    async def _add_skill(self) -> ResourceSkillSchema:
        skill = ResourceSkillModel(**self._data.model_dump())
        self._ses.add(skill)
        await self._ses.commit()
        await self._ses.refresh(skill)
        return ResourceSkillSchema.model_validate(skill, from_attributes=True)

    async def execute(self) -> ResourceSkillSchema:
        return await self._add_skill()
