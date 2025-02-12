from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import Connection, select

from app.config import main_config
from app.deps import get_db
from app.schemas import AccessTokenData, UserInternal
from app.models import users_table

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(fake_db, username: str, password: str):
    user = get_user_by_username(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def get_user_by_username(db_conn: Connection, username: str | None) -> UserInternal | None:
    if not username:
        return
    db_user = db_conn.execute(select(users_table).where(users_table.c.username == username))
    user = db_user.one_or_none()
    if not user:
        return
    return UserInternal(**user.__dict__)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, main_config.jwt_secret_key, algorithm=main_config.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_conn: Annotated[Connection, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, main_config.jwt_secret_key, algorithms=[main_config.jwt_algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = AccessTokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db_conn, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[Any, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

