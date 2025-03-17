from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlmodel import select

from app import models
from app.deps import SessionDep, CurrentUserDep, get_current_user
from app.config import limiter
from app import crud

items_router = APIRouter(prefix="/items", tags=["items"])


@limiter.limit("5/minute")
@items_router.get(
    "/",
    response_model=models.ItemsPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def get_items(
    request: Request,
    session: SessionDep,
    current_user: CurrentUserDep,
    offset: int = Query(default=0, gt=-1),
    limit: int = 100,
):
    _ = request
    items = session.exec(
        select(models.Item)
        .where(models.Item.owner_id == current_user.id)
        .offset(offset)
        .limit(limit)
    ).all()
    return models.ItemsPublic(
        data=[models.ItemPublic(**item.model_dump()) for item in items]
    )


@limiter.limit("5/minute")
@items_router.get(
    "/{item_id}",
    response_model=models.ItemPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def get_item(
    request: Request,
    session: SessionDep,
    current_user: CurrentUserDep,
    item_id: UUID,
):
    _ = request
    item = session.exec(
        select(models.Item).where(models.Item.id == item_id)
    ).one_or_none()
    if not item or item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item with this id not found",
        )
    return models.ItemPublic(**item.model_dump())


@limiter.limit("5/minute")
@items_router.post(
    "/",
    response_model=models.ItemPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
def create_item(
    request: Request,
    session: SessionDep,
    current_user: CurrentUserDep,
    item_create: models.ItemCreate,
):
    _ = request
    item = crud.create_item(session, item_create, current_user.id)
    return models.ItemPublic(**item.model_dump())
