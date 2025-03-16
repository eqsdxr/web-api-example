from fastapi import APIRouter

from app.config import get_settings
from app.routes.v1.login import login_router
from app.routes.v1.private import private_router
from app.routes.v1.users import users_router
from app.routes.v1.utils import utils_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(login_router)
v1_router.include_router(users_router)
v1_router.include_router(utils_router)

if get_settings().ENVIRONMENT == "local":
    v1_router.include_router(private_router)
