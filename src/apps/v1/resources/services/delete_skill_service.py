from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.exceptions import SkillHttpExceptionTypeEnum, skill_exception_fabric
from src.apps.v1.resources.models import ResourceSkillModel


class DeleteSkillService:
    def __init__(self, skill_id: int, session: AsyncSession) -> None:
        self._skill_id = skill_id
        self._ses = session

    async def _delete_skill(self) -> None:
        skill = await self._ses.get(ResourceSkillModel, self._skill_id)
        if skill is None:
            raise skill_exception_fabric(SkillHttpExceptionTypeEnum.SKILL_NOT_FOUND)

        await self._ses.delete(skill)
        await self._ses.commit()

    async def execute(self) -> None:
        await self._delete_skill()
