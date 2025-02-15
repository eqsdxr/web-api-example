from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app import crud
from app.models import (
    MultipleUsersResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
    Message,
    UsersTable,
)
from app.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MultipleUsersResponse,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(UsersTable)
    count = session.exec(count_statement).one()

    statement = select(UsersTable).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return MultipleUsersResponse(
        users=[UserResponse(**u.model_dump()) for u in users], count=count
    )


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserResponse,
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    session: SessionDep, current_user: CurrentUser, user_id: UUID
) -> Any:
    user = session.get(UsersTable, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserResponse,
)
def update_user(
    *,
    session: SessionDep,
    user_id: UUID,
    user_in: UserUpdate,
) -> Any:
    db_user = session.get(UsersTable, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = crud.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = crud.update_user(
        session=session, db_user=db_user, user_in=user_in
    )
    return db_user


@router.delete(
    "/{user_id}", dependencies=[Depends(get_current_active_superuser)]
)
def delete_user(
    session: SessionDep, current_user: CurrentUser, user_id: UUID
) -> Message:
    user = session.get(UsersTable, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403,
            detail="Super users are not allowed to delete themselves",
        )
    session.delete(user)
    session.commit()
    return Message(text="User deleted successfully")
