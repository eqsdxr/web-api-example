from fastapi.testclient import TestClient
from app.config import get_settings
from app.crud import create_user
from app.models import UserCreate, User
from app.db import engine
from sqlmodel import SQLModel, Session, select


def init_db(session: Session):
    # Create tables
    SQLModel.metadata.create_all(engine)
    # Create superuser
    user = session.exec(
        select(User).where(
            User.username == get_settings().FIRST_SUPERUSER_USERNAME
        )
    ).first()
    if not user:
        user_create = UserCreate(
            username=get_settings().FIRST_SUPERUSER_USERNAME,
            password=get_settings().FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = create_user(session=session, user_create=user_create)


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": get_settings().FIRST_SUPERUSER_USERNAME,
        "password": get_settings().FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("api/v1/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
