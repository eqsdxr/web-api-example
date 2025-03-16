from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select

from app.config import limiter, logger
from app import crud
from app.deps import (
    CurrentUserDep,
    SessionDep,
    SuperuserDep,
    get_current_superuser,
    get_current_user,
)
from app.models import User, UserCreate, UserPublic, UsersPublic, UserUpdate

users_router = APIRouter(prefix="/users", tags=["user"])


@logger.catch  # Catch unexpected exceptions
@users_router.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
@limiter.limit("5/minute")
async def get_user_me(
    current_user: CurrentUserDep,
    request: Request,
) -> UserPublic:
    _ = request
    return UserPublic(**current_user.model_dump())


@logger.catch
@users_router.get(
    "/",
    response_model=UsersPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
@limiter.limit("5/minute")
async def get_users(
    request: Request,
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> UsersPublic:
    _ = request
    result = crud.retrieve_users(session, offset, limit)
    return result


@logger.catch
@users_router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_superuser)],
)
@limiter.limit("5/minute")
async def create_user(
    request: Request,
    session: SessionDep,
    user: UserCreate,
) -> UserPublic:
    _ = request
    if user.username:
        user_with_this_username = session.exec(
            select(User).where(User.username == user.username)
        ).first()
        if user_with_this_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
    created_user = crud.create_user(session, user)
    return UserPublic(**created_user.model_dump())


@logger.catch
@users_router.patch(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_superuser)],
)
@limiter.limit("5/minute")
async def update_user_me(
    request: Request,
    current_superuser: SuperuserDep,
    session: SessionDep,
    user_update: UserUpdate,
) -> UserPublic:
    _ = request
    if user_update.username:
        user_with_this_username = session.exec(
            select(User).where(User.username == user_update.username)
        ).first()
        if user_with_this_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
    user = session.exec(
        select(User).where(User.id == current_superuser.id)
    ).one()
    updated_user = crud.update_user(session, user, user_update)
    return UserPublic(**updated_user.model_dump())


@logger.catch
@users_router.patch(
    "/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_superuser)],
)
@limiter.limit("5/minute")
async def update_user(
    request: Request,
    session: SessionDep,
    user_id: UUID,
    user_update: UserUpdate,
) -> UserPublic:
    _ = request
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id not found",
        )
    if user_update.username:
        user_with_this_username = session.exec(
            select(User).where(User.username == user_update.username)
        ).first()
        if user_with_this_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
    updated_user = crud.update_user(session, user, user_update)
    return UserPublic(**updated_user.model_dump())


@logger.catch
@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_superuser)],
)
@limiter.limit("5/minute")
async def delete_user(
    request: Request,
    user_id: UUID,
    session: SessionDep,
    current_superuser: SuperuserDep,
) -> str:
    _ = request
    if user_id == current_superuser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Superusers are not allowed to delete themselves",
        )
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id not found",
        )
    crud.delete_user(session, user)
    return f"User with id {user_id} deleted successfully"
