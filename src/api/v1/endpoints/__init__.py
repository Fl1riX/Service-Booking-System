from fastapi import APIRouter
from .users import router as users_router
from .entrepreneurs import router as entrepreneurs_router
from .services import router as entrepreneurs_router
from .appointments import router as appointments_router

router = APIRouter()
router.include_router(users_router)
router.include_router(entrepreneurs_router)
router.include_router(entrepreneurs_router)
router.include_router(appointments_router)