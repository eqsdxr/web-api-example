from fastapi import HTTPException, status
from sqlmodel import Session, func, select

from app.models import User, UserCreate, UserPublic, UsersPublic, UserUpdate
from app.sec import get_password_hash, verify_password


def authenticate(session: Session, username: str, password: str) -> User:
    user = session.exec(
        select(User).where(User.username == username)
    ).one_or_none()
    # Keep users unaware if the password is wrong or the user doesn't exist
    # for security reasons
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid credentials"
        )
    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(
    session: Session, db_user: User, user_update: UserUpdate
) -> User:
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
) -> UsersPublic:
    db_users = session.exec(select(User).offset(offset).limit(limit))
    users = [UserPublic(**db_user.model_dump()) for db_user in db_users]
    count = session.exec(select(func.count()).select_from(User)).one()
    return UsersPublic(count=count, users=users)


def delete_user(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
    session.expire_all()
