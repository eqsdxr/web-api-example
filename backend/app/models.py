from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    Text,
    Uuid,
)

metadata = MetaData()

users_table = Table(
    "users_table",
    metadata,
    Column("id", Uuid, primary_key=True, unique=True),
    Column("username", String(50), index=True, nullable=False, unique=True),
    Column("password_hash", String(255), nullable=False),
    Column("bio", Text, nullable=True),
)
