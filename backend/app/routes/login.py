from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config import main_config
from app.models import AccessToken, UserResponse
from app.sec import create_access_token
from app.deps import CurrentUser, SessionDep
from app.crud import authenticate

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=AccessToken)
async def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AccessToken:
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=main_config.access_token_duration_hours)
    return AccessToken(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserResponse)
def test_token(current_user: CurrentUser) -> Any:
    return current_user



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
