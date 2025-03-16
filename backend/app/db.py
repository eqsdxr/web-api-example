from sqlmodel import create_engine

from app.config import get_settings


engine = create_engine(get_settings().DATABASE_URI)
