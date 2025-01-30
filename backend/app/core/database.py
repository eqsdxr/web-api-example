from asyncio import run

from databases import Database
from sqlalchemy import insert

from app.core.security import hash_password
from app.core.database import database
from app.core.models import users_table
from app.core.configuration import app_config

database = Database(app_config["database_url"])

async def create_admin() -> None:
    query = insert(users_table).values(
        username=app_config["admin_username"],
        email=app_config["admin_email"],
        hashed_password=hash_password(app_config["admin_password"]),
    )
    await database.execute(query=query)

if __name__ == "__main__":
    run(create_admin())
