import secrets
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import func, select

from app.crud import create_db_user, get_user_by_email, get_user_by_username
from app.deps import SessionDep
from app.models import UserCreate, UserResponse, UsersTable

router = APIRouter(prefix="/development", tags=["development"])


@router.get("/check-api")
async def check_api():
    return "OK"


@router.get("/check-db")
async def check_database_connection(session: SessionDep):
    count_statement = select(func.count()).select_from(UsersTable)
    count = session.exec(count_statement).one()
    return {"amount_of_users_in_system": count}


@router.post("/create-user-dev")
async def create_user_dev(
    session: SessionDep, user: UserCreate, superuser=False
):
    user.is_superuser = superuser
    user.is_active = True  # Should I remove this field completely?
    created_user = create_db_user(session=session, user_create=user)
    return UserResponse(**created_user.model_dump())


@router.post("/seed-users")
async def seed_users_database(
    session: SessionDep,
    amount_of_users: Annotated[int, Query(gt=0, lt=50)] = 1,
) -> str:
    seeded_count = 0

    for _ in range(amount_of_users):
        while True:
            rn = secrets.randbelow(10_000_000)
            email = f"random{rn}@seeded.com"
            username = f"user{rn}"

            if not get_user_by_email(
                session, email
            ) and not get_user_by_username(session, username):
                break

        random_user = UserCreate(
            email=email,
            username=username,
            password="password",
        )
        create_db_user(session=session, user_create=random_user)
        seeded_count += 1

    return f"{seeded_count} users were seeded into the database"
