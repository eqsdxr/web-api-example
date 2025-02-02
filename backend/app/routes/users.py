from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import Connection, text

from app.deps import get_db
from app.schemas import (
    MultipleUsersReadResponse,
    UserCreate,
    UserCreateResponse,
    UserDeleteResponse,
    SingleUserReadResponse,
    UserUpdate,
    UserUpdateResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/testing")
def testing(conn: Annotated[Connection, Depends(get_db)]):
    result = conn.execute(text("SELECT * FROM users_table;"))
    rows = result.fetchall()  # Fetch all rows
    return {"something": [dict(row) for row in rows]}


@router.get("/{user_id}", response_model=SingleUserReadResponse)
async def read_single_user(user_id: UUID) -> SingleUserReadResponse:
    pass


@router.get("/", response_model=MultipleUsersReadResponse)
async def read_multiple_users(
    skip: int = 0,
    limit: int = 10,
) -> MultipleUsersReadResponse:
    pass


@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreate) -> UserCreateResponse:
    pass


@router.patch("/{user_id}", response_model=UserUpdateResponse)
def update_user(user_id: UUID, user: UserUpdate) -> UserUpdateResponse:
    pass


@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: UUID) -> UserDeleteResponse:
    pass
