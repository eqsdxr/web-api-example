from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Connection, insert, select

from app.deps import get_db
from app.models import users_table
from app.schemas import (
    UserCreate,
    UserCreateResponse,
)
from app.sec import hash_password

router = APIRouter(prefix="/users", tags=["users"])

#@router.get("/{user_id}", response_model=SingleUserReadResponse)
#async def read_single_user(
#    user_id: UUID, conn: Annotated[Connection, Depends(get_db)]
#) -> SingleUserReadResponse:
#    user = conn.execute(select(user_table).where(user_table.id == user_id))
#
#
#@router.get("/", response_model=MultipleUsersReadResponse)
#async def read_multiple_users(
#    conn: Annotated[Connection, Depends(get_db)],
#    skip: int = 0,
#    limit: int = 10,
#) -> MultipleUsersReadResponse:
#    pass
#

@router.post("/", response_model=UserCreateResponse)
def create_user(
    user: UserCreate, conn: Annotated[Connection, Depends(get_db)]
    ) -> UserCreateResponse:
    email = conn.execute(select(users_table).where(users_table.c.email == user.email))
    print(email)
    if email.first():
        raise HTTPException(409, "This email has already been registered.")
    username = conn.execute(select(users_table).where(users_table.c.username == user.username))
    if username.first():
        raise HTTPException(409, "This username has already been registered.")
    stmt = insert(users_table).values(
        bio=user.bio, 
        created_at=datetime.now(timezone.utc),
        email=user.email,
        id=uuid4(),
        is_activated=False,
        password_hash=hash_password(user.password), 
        username=user.username 
    )
    conn.execute(stmt)
    conn.commit()
    return UserCreateResponse(**user.model_dump())


#@router.patch("/{user_id}", response_model=UserUpdateResponse)
#def update_user(
#    user_id: UUID,
#    data: UserUpdate,
#    conn: Annotated[Connection, Depends(get_db)],
#) -> UserUpdateResponse:
#    pass
#
#
#@router.delete("/{user_id}", response_model=UserDeleteResponse)
#def delete_user(
#    user_id: UUID, conn: Annotated[Connection, Depends(get_db)]
#) -> UserDeleteResponse:
#    pass
