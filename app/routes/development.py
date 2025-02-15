from typing import Annotated
import secrets

from fastapi import APIRouter, Query
from sqlmodel import select, func

from app.deps import SessionDep
from app.models import UserCreate, UsersTable
from app.crud import get_user_by_email, create_user, get_user_by_username

router = APIRouter(prefix="/development", tags=["development"])


@router.get("/check-api")
async def check_api():
    return "OK"


@router.get("/check-db")
async def check_database_connection(session: SessionDep):
    count_statement = select(func.count()).select_from(UsersTable)
    count = session.exec(count_statement).one()
    return {"amount_of_users_in_system": count}


@router.post("/seed-users")
async def seed_users_database(
    session: SessionDep,
    amount_of_users: Annotated[int, Query(gt=0, lt=50)] = 1,
):
    seeded_count = 0

    for _ in range(amount_of_users):
        while True:
            rn = secrets.randbelow(10_000_000)
            email = f"random{rn}@seeded.com"
            username = f"user{rn}"

            if not get_user_by_email(session, email) and not get_user_by_username(session, username):
                break

        random_user = UserCreate(
            email=email,
            username=username,
            password="password",
        )
        create_user(session=session, user_create=random_user)
        seeded_count += 1

    return f"{seeded_count} users were seeded into the database"

