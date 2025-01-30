from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import (
    insert,
)

from app.core.security import hash_password
from app.core.schemas import UserCreate, UserResponse
from app.core.dependencies import (
    get_current_user_dependency,
    get_database_connection,
)
from app.core.models import users_table

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_users_me(
    # TODO replace Any with sth
    current_user: Annotated[Any, Depends(get_current_user_dependency)],
    database_connection=Depends(get_database_connection),
):
    return ""


@router.get("/")
def read_users(database_connection=get_database_connection()):
    return "OK"


@router.post("/", response_model=UserResponse)
def create_user(
    # TODO replace Any with sth
    current_user: Annotated[Any, Depends(get_current_user_dependency)],
    user: UserCreate,
    database_connection=Depends(get_database_connection),
):
    hashed_password = hash_password(user.password)
    query = insert(users_table).values(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    result = database_connection.execute(query=query)
    return {"id": result.lastrowid, **user.model_dump()}


@router.put("/")
def update_user():
    pass


@router.delete("/")
def delete_user():
    pass
