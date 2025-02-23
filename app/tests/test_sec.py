from datetime import timedelta, datetime, timezone

import pytest
import jwt

from app import sec
from app.config import main_config


def test_get_password_hash():
    password = "testtest"
    hashed_password = sec.get_password_hash(password)
    assert password != hashed_password


def test_verify_password():
    password = "testtest"
    hashed_password = sec.get_password_hash(password)
    assert sec.verify_password(password, hashed_password)


def test_create_access_token():
    subject = "test_user"
    expires_delta = timedelta(minutes=15)
    token = sec.create_access_token(subject, expires_delta)

    decoded_payload = jwt.decode(
        token,
        main_config.jwt_secret_key,
        algorithms=[main_config.jwt_algorithm],
    )
    assert decoded_payload["subject"] == subject

    exp_timestamp = decoded_payload["exp"]
    exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    expected_exp_time = datetime.now(timezone.utc) + expires_delta
    assert exp_time.timestamp() == pytest.approx(expected_exp_time.timestamp())
