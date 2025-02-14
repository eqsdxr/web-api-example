from random import randint
from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Connection, text, insert

from app.deps import get_db
from app.sec import hash_password
from app.models import users_table

router = APIRouter(prefix="/development", tags=["development"])


@router.get("/check")
def check_api():
    return "OK"


@router.get("/database")
def check_database_connection(conn: Annotated[Connection, Depends(get_db)]):
    result = conn.execute(text("SELECT * FROM users_table;"))
    return {"something": [dict(row) for row in result.mappings()]}


@router.post("/seed")
def seed_users_database(
    conn: Annotated[Connection, Depends(get_db)],
    amount_of_users: Annotated[int, Query(gt=-1, lt=200)] = 0,
) -> str | None:
    for _ in range(amount_of_users):
        rn = randint(100000, 10000000)
        stmt = insert(users_table).values( # TODO Add default factory to schemas for some fields
            created_at=datetime.now(timezone.utc),
            email=f"user{rn}@example.com",
            id=uuid4(),
            is_activated=False,
            password_hash=hash_password("password"),
            username=f"user{rn}"
        )
        conn.execute(stmt)
    conn.commit()
    return f"{amount_of_users} users were seeded into database."
