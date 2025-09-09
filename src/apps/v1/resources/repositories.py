from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.models import ResourceSkillModel


class SkillRepository:
    def __init__(self, session: AsyncSession):
        self._ses = session

    async def get_by_id(self, skill_id: int) -> ResourceSkillModel | None:
        return await self._ses.get(ResourceSkillModel, skill_id)  # type: ignore

    async def get_items(self) -> ScalarResult[ResourceSkillModel]:
        q = select(ResourceSkillModel)
        return (await self._ses.execute(q)).scalars()

    async def save(self, skill: ResourceSkillModel) -> None:
        self._ses.add(skill)
        await self._ses.commit()
        await self._ses.refresh(skill)
