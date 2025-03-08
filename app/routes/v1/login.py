from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestFormStrict

from app.config import get_settings, limiter, logger
from app.crud import authenticate
from app.deps import SessionDep
from app.models import Token
from app.sec import check_and_rehash, create_access_token

login_router = APIRouter(prefix="/login", tags=["login"])


@logger.catch
@login_router.post(
    "/access-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
) -> Token:
    _ = request  # Stop showing the warning
    user = authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    # Recommended Argon2 rehashing logic during login
    # https://pypi.org/project/argon2-cffi/
    check_and_rehash(session, user, form_data.password)
    access_token_expires = timedelta(
        minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
