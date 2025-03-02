from sqlmodel import Session, create_engine, select

from app.config import get_settings
from app.crud import create_user
from app.models import User, UserCreate


def create_tables(engine):
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


def create_first_user(session: Session):
    user = session.exec(
        select(User).where(
            User.username == get_settings().first_superuser_username
        )
    ).first()
    if not user:
        user_create = UserCreate(
            username=get_settings().first_superuser_username,
            password=get_settings().first_superuser_password,
        )
        user = create_user(session=session, user_create=user_create)


engine = create_engine(get_settings().database_uri)
