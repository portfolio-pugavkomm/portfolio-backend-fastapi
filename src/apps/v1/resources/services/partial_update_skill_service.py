from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.exceptions import SkillHttpExceptionTypeEnum, skill_exception_fabric
from src.apps.v1.resources.repositories import SkillRepository
from src.apps.v1.resources.schemas import ResourceSkillPartialSchema, ResourceSkillSchema
from src.utils import update_model_attributes_from_dict


class PartialUpdateSkillService:
    def __init__(self, skill_id: int, data: ResourceSkillPartialSchema, session: AsyncSession) -> None:
        self._skill_id = skill_id
        self._data = data
        self._repo = SkillRepository(session=session)

    async def _update_skill(self) -> ResourceSkillSchema:
        skill = await self._repo.get_by_id(self._skill_id)
        if not skill:
            raise skill_exception_fabric(SkillHttpExceptionTypeEnum.SKILL_NOT_FOUND)

        data = self._data.model_dump(exclude_none=True)
        update_model_attributes_from_dict(skill, data)
        await self._repo.save(skill)

        return ResourceSkillSchema.model_validate(skill, from_attributes=True)

    async def execute(self) -> ResourceSkillSchema:
        return await self._update_skill()
