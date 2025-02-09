from typing import Annotated

from fastapi import APIRouter, Form

from app.schemas import LoginForm

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
async def login(credentials: Annotated[LoginForm, Form()]):
    return "access_code"


#@router.post("/", response_model=)
#async def logout() -> :
#   pass
#
#
#@router.put("/update-email", response_model=)
#async def update_email() -> :
#   pass
#
#
#@router.put("/update-password", response_model=)
#async def update_password() -> :
#   pass
#
#
#@router.put("/update-username", response_model=)
#async def update_username() -> :
#   pass
#
#
