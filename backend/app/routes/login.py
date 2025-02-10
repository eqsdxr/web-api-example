from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config import main_config
from app.schemas import AccessToken

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=AccessToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=main_config["access_token_duration_hours"])
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return AccessToken(access_token=access_token, token_type="bearer")

# @router.post("/", response_model=)
# async def logout() -> :
#   pass
#
#
# @router.put("/update-email", response_model=)
# async def update_email() -> :
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
