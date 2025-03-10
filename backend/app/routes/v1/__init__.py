from fastapi import APIRouter

from app.routes.v1.login import login_router
from app.routes.v1.metadata import metadata_router
from app.routes.v1.user import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(login_router)
v1_router.include_router(metadata_router)
v1_router.include_router(user_router)
