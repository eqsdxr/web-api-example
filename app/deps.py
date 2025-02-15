from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.config import main_config
from app.models import AcessTokenPayload, UsersTable
from app.db import get_db_session

# Should be the same as login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login/")


SessionDep = Annotated[Session, Depends(get_db_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> UsersTable:
    try:
        payload = jwt.decode(
            token,
            main_config.jwt_secret_key,
            algorithms=[main_config.jwt_algorithm],
        )
        token_data = AcessTokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(UsersTable, token_data.subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[UsersTable, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> UsersTable:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
