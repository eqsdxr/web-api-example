from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import Connection, text

from app.deps import get_db

router = APIRouter(prefix="/development", tags=["development"])

@router.get("/")
def check_database_connection(conn: Annotated[Connection, Depends(get_db)]):
    result = conn.execute(text("SELECT * FROM users_table;"))
    return {"something": [dict(row) for row in result.mappings()]}


