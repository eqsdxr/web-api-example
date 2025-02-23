from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config import main_config
from app.crud import authenticate
from app.deps import SessionDep
from app.models import AccessToken
from app.sec import create_access_token

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token", response_model=AccessToken)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    user = authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=main_config.access_token_duration_hours
    )
    return AccessToken(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


# @router.post("/", response_model=)
# async def logout() -> :
#   pass
#
#
# @router.put("/update-password", response_model=)
# async def update_password() -> :
#   pass
#
#
# @router.put("/update-username", response_model=)
# async def update_username() -> :
#   pass
#
#
