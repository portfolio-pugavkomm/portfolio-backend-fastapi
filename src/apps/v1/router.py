from fastapi import APIRouter

from .auth.router import router as auth_router
from .resources.router import router as resources_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(resources_router)
