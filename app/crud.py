from typing import Any

from sqlmodel import Session, select

from app.sec import get_password_hash, verify_password
from app.models import UsersTable, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> UsersTable:
    db_obj = UsersTable.model_validate(
        user_create,
        update={"password_hash": get_password_hash(user_create.password)},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(
    *, session: Session, stored_user: UsersTable, user: UserUpdate
) -> Any:
    user_data = user.model_dump(exclude_unset=True, exclude_none=True)
    extra_data = {}
    if "password" in user_data:
        extra_data["password_hash"] = get_password_hash(user_data["password"])
    stored_user.sqlmodel_update(user_data, update=extra_data)
    session.add(stored_user)
    session.commit()
    session.refresh(stored_user)
    return stored_user


def get_user_by_email(session: Session, email: str) -> UsersTable | None:
    statement = select(UsersTable).where(UsersTable.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_username(session: Session, username: str) -> UsersTable | None:
    statement = select(UsersTable).where(UsersTable.username == username)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(
    *, session: Session, email_or_username: str, password: str
) -> UsersTable | None:
    if "@" in email_or_username:
        db_user = get_user_by_email(session=session, email=email_or_username)
    else:
        db_user = get_user_by_username(session=session, username=email_or_username)
    if not db_user:
        return None
    if not verify_password(password, db_user.password_hash):
        return None
    return db_user
