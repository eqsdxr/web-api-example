from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session, func, select

from app import models
from app.sec import get_password_hash, verify_password


def authenticate(
    session: Session, username: str, password: str
) -> models.User:
    user = session.exec(
        select(models.User).where(models.User.username == username)
    ).one_or_none()
    # Keep users unaware if the password is wrong or the user doesn't exist
    # for security reasons
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid credentials"
        )
    return user


def create_user(
    session: Session, user_create: models.UserCreate
) -> models.User:
    db_obj = models.User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(
    session: Session, db_user: models.User, user_update: models.UserUpdate
) -> models.User:
    data = user_update.model_dump(exclude_unset=True)
    extra = {}
    if "password" in data:
        extra["hashed_password"] = get_password_hash(data["password"])
    db_user.sqlmodel_update(data, update=extra)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def retrieve_users(
    session: Session, offset: int = 0, limit: int = 100
) -> models.UsersPublic:
    db_users = session.exec(select(models.User).offset(offset).limit(limit))
    users = [models.UserPublic(**db_user.model_dump()) for db_user in db_users]
    count = session.exec(select(func.count()).select_from(models.User)).one()
    return models.UsersPublic(count=count, users=users)


def delete_user(session: Session, user: models.User) -> None:
    session.delete(user)
    session.commit()
    session.expire_all()


def create_item(
    session, item_create: models.ItemCreate, owner_id: UUID
) -> models.Item:
    db_item = models.Item.model_validate(
        item_create, update={"owner_id": owner_id}
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
