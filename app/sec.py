from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from app.config import get_settings

ph = PasswordHasher()


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire: datetime = datetime.now(timezone.utc) + expires_delta
    to_encode = {"subject": str(subject), "expire": expire.isoformat()}
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().JWT_SECRET,
        algorithm=get_settings().JWT_ALGORITHM,
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerificationError, VerifyMismatchError, InvalidHashError):
        return False
