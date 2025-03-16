from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, decode
from pydantic import ValidationError
from sqlmodel import Session

from app.config import get_settings
from app.db import engine
from app.models import TokenPayload, User


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/login/access-token")

SessionDep = Annotated[Session, Depends(get_db)]

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep):
    try:
        payload = decode(
            token,
            get_settings().JWT_SECRET,
            algorithms=[get_settings().JWT_ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.subject)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return User(**user.model_dump())


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_current_superuser(user: CurrentUserDep):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough rights",
        )
    return user


SuperuserDep = Annotated[User, Depends(get_current_superuser)]
