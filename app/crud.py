from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import User, UserCreate
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
