from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.v1.resources.repositories import SkillRepository
from src.apps.v1.resources.schemas import ResourceSkillSchema


class GetAllResourcesService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = SkillRepository(session)

    async def _get_resources_list(self) -> list[ResourceSkillSchema]:
        result = await self._repo.get_items()
        return [ResourceSkillSchema.model_validate(row, from_attributes=True) for row in result]

    async def execute(self) -> list[ResourceSkillSchema]:
        return await self._get_resources_list()
