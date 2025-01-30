from typing import Annotated

from databases import Database
from fastapi import Depends

from app.core.security import oauth2_scheme
from app.core.database import database

async def get_database_connection() -> Database:
    return database


async def get_current_user_dependency(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    pass
