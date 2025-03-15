from sqlmodel import Session, create_engine, select

from app.config import get_settings
from app.crud import create_user
from app.models import User, UserCreate


def create_tables(engine):
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


def create_first_superuser_if_doesnt_exist(session: Session):
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


engine = create_engine(get_settings().DATABASE_URI)
