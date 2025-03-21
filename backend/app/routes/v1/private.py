from fastapi import APIRouter

from app.crud import create_user
from app.deps import SessionDep
from app.models import UserCreate

private_router = APIRouter(prefix="/private", tags=["private"])


@private_router.post("/create-user")
async def create_user_private(session: SessionDep, user: UserCreate):
    created_user = create_user(session, user)
    return created_user
