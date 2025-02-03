from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    Text,
    Uuid,
)

metadata = MetaData()

user_table = Table(
    "user_table",
    metadata,
    Column("id", Uuid, primary_key=True, unique=True),
    Column("username", String(50), index=True, nullable=False, unique=True),
    Column("password_hash", Text, nullable=False),
    Column("bio", Text, nullable=True),
)
