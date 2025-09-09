from fastapi import APIRouter, Depends

from src.apps.v1.auth.dependencies import admin_required
from src.apps.v1.resources.schemas import AddResourceSkillSchema, ResourceSkillPartialSchema, ResourceSkillSchema
from src.apps.v1.resources.services import (
    AddSkillService,
    DeleteSkillService,
    GetAllResourcesService,
    PartialUpdateSkillService,
    UpdateSkillService,
)
from src.dependencies import DBSessionDep
from src.tags import RESOURCES_TAG

router = APIRouter(
    prefix="/resources",
    tags=[
        RESOURCES_TAG,
    ],
)


@router.get(
    "/skills",
)
async def skills_list(ses: DBSessionDep) -> list[ResourceSkillSchema]:
    """# Get list of skills

    This endpoint available for all users
    """
    return await GetAllResourcesService(ses).execute()


@router.post("/skills", dependencies=(Depends(admin_required),))
async def add_skill(data: AddResourceSkillSchema, ses: DBSessionDep) -> ResourceSkillSchema:
    """# Create skill

    Available for the next users:
    - admin

    """
    return await AddSkillService(data, ses).execute()


@router.put(
    "/skills/{skill_id}",
    responses={"404": {"description": "Not found instance"}},
    dependencies=(Depends(admin_required),),
)
async def update_skill(
    skill_id: int,
    data: AddResourceSkillSchema,
    ses: DBSessionDep,
) -> ResourceSkillSchema:
    """# Update skill data

    Available for the next users:

    - admin
    """
    return await UpdateSkillService(skill_id, data, ses).execute()


@router.patch(
    "/skills/{skill_id}",
    responses={"404": {"description": "Not found instance"}},
    dependencies=(Depends(admin_required),),
)
async def partial_update_skill(
    skill_id: int,
    data: ResourceSkillPartialSchema,
    ses: DBSessionDep,
) -> ResourceSkillSchema:
    """# Partial update skill data

    Available for the next users:

    - admin
    """
    return await PartialUpdateSkillService(skill_id, data, ses).execute()


@router.delete(
    "/skills/{skill_id}",
    dependencies=(Depends(admin_required),),
)
async def delete_skill(skill_id: int, ses: DBSessionDep) -> None:
    return await DeleteSkillService(skill_id, ses).execute()
