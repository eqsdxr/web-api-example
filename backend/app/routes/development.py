from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Connection, text

from app.deps import get_db

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
    # TODO - Add user seeding logic
    return f"{amount_of_users} users were seeded into database."
