from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.repositories import SkillRepository
from src.apps.v1.resources.schemas import AddResourceSkillSchema, ResourceSkillSchema
from src.utils import update_model_attributes_from_dict


class UpdateSkillService:
    def __init__(self, skill_id: int, data: AddResourceSkillSchema, session: AsyncSession) -> None:
        self._skill_id = skill_id
        self._data = data
        self._repo = SkillRepository(session)

    async def _update_skill(self) -> ResourceSkillSchema:
        skill = await self._repo.get_by_id(self._skill_id)
        if not skill:
            raise HTTPException(404, detail="Skill not found")
        update_model_attributes_from_dict(skill, self._data.model_dump())
        await self._repo.save(skill)
        return ResourceSkillSchema.model_validate(skill, from_attributes=True)

    async def execute(self) -> ResourceSkillSchema:
        return await self._update_skill()
