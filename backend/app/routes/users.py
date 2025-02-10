from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Connection, insert, select

from app.deps import get_db
from app.models import users_table
from app.schemas import (
    MultipleUsersResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.sec import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def read_single_user(
    user_id: UUID, conn: Annotated[Connection, Depends(get_db)]
) -> UserResponse:
    user = conn.execute(select(users_table).where(users_table.c.id == user_id))
    return UserResponse(**user.__dict__)  # Check if it works


@router.get("/", response_model=MultipleUsersResponse)
async def read_multiple_users(
    conn: Annotated[Connection, Depends(get_db)],
    offset: int = 0,
    limit: int = 10,
) -> MultipleUsersResponse:
    users = conn.execute(select(users_table).offset(offset).limit(limit))
    return MultipleUsersResponse(**users.__dict__)  # Check if it works


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, conn: Annotated[Connection, Depends(get_db)]
) -> UserResponse:
    email = conn.execute(
        select(users_table).where(users_table.c.email == user.email)
    )
    if email.first():
        raise HTTPException(409, "This email has already been registered.")
    username = conn.execute(
        select(users_table).where(users_table.c.username == user.username)
    )
    if username.first():
        raise HTTPException(409, "This username has already been registered.")
    stmt = insert(users_table).values(
        bio=user.bio,
        created_at=datetime.now(timezone.utc),
        email=user.email,
        id=uuid4(),
        is_activated=False,
        password_hash=hash_password(user.password),
        username=user.username,
    )
    conn.execute(stmt)
    conn.commit()
    return UserResponse(**user.model_dump())


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    conn: Annotated[Connection, Depends(get_db)],
) -> UserResponse:
    user = conn.execute(select(users_table).where(users_table.c.id == user_id))
    if not user.first():
        raise HTTPException(404, "User not found.")
    if user_data.password:
        user_data.password = hash_password(user_data.password)
    updated_data = user_data.model_dump(exclude_unset=True)
    # TODO - add updating logic
    return UserResponse(**user_data.model_dump())


# @router.delete("/{user_id}", response_model=UserDeleteResponse)
# def delete_user(
#    user_id: UUID, conn: Annotated[Connection, Depends(get_db)]
# ) -> UserDeleteResponse:
#    pass
