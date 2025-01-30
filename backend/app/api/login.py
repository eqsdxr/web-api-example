from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_database_connection
from app.core.security import authenticate_user, create_access_jwt_token

router = APIRouter(prefix="/login", tags=["login"])


@router.get("/")
async def login(
    form_input_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    database_connection=Depends(get_database_connection),
):
    user: dict[str, Any] | Literal[False] = await authenticate_user(
        username_or_email=form_input_data.username,
        user_password=form_input_data.password,
        database_connection=database_connection
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or email or password")

    jwt_access_token = await create_access_jwt_token(data=user)

    return jwt_access_token
