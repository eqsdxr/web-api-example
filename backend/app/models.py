from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    Text,
    Uuid,
    DateTime,
    Boolean,
)

metadata = MetaData()

users_table = Table(
    "users_table",
    metadata,
    Column("bio", Text, nullable=True),
    Column("created_at", DateTime, nullable=False),
    Column("email", String(50), index=True, nullable=False, unique=True),
    Column("id", Uuid, primary_key=True, unique=True),
    Column("is_activated", Boolean, default=False, nullable=False),
    Column("password_hash", Text, nullable=False),
    Column("username", String(50), index=True, nullable=False, unique=True),
)
