from typing import Any
from datetime import timedelta, datetime, UTC

from jwt import decode, DecodeError, encode
from bcrypt import checkpw, hashpw, gensalt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.core.configuration import app_config
from app.core.models import users_table

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_correct: bool = checkpw(
        plain_password.encode(), hashed_password.encode()
    )
    return is_correct


async def hash_password(password: str) -> str:
    hashed_password: str = hashpw(password.encode(), gensalt()).decode()
    return hashed_password


# TODO
async def verify_jwt_token(token):
    try:
        payload = decode(
            token,
            app_config["secret_jwt_key"],
            algorithms=[app_config["jwt_algorithm"]],
        )
        return  # Return what?
    except DecodeError:
        return  # Return what?


async def create_access_jwt_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(
            hours=app_config["access_token_duration_hours"]
        )
    data_to_encode.update({"expire": expire})
    encoded_jwt_token: str = encode(
        payload=data_to_encode,
        key=app_config["secret_jwt_key"],
        algorithm=app_config["jwt_algorithm"],
    )
    return encoded_jwt_token


async def authenticate_user(
    username_or_email: str, user_password: str, database_connection
):
    if "@" in username_or_email:
        query = select(users_table).where(
            users_table.c.email == username_or_email
        )
    else:
        query = select(users_table).where(
            users_table.c.username == username_or_email
        )
    database_user: dict[str, Any] | None = await database_connection.fetch_one(query=query)

    if not database_user:
        return False

    if not await verify_password(
        user_password, database_user["hashed_password"]
    ):
        return False

    return database_user

