from datetime import datetime, timezone
from uuid import uuid4

from pydantic import EmailStr
from sqlmodel import UUID, SQLModel, Field


class LoginForm(SQLModel):
    # Does it work well?
    email_username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=50)


class AccessToken(SQLModel):
    access_token: str
    token_type: str = "bearer"


class AcessTokenPayload(SQLModel):
    username: str | None = None


class UserBase(SQLModel):
    bio: str | None = Field(default=None, max_length=1500)
    email: EmailStr
    username: str = Field(min_length=4, max_length=50)
    is_active: bool = False
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserInternal(UserBase):
    created_at: datetime
    password_hash: str


class UserResponse(UserBase):
    created_at: datetime


class MultipleUsersResponse(SQLModel):
    count: int
    users: list[UserResponse]


class UserUpdate(SQLModel):
    bio: str | None = Field(default=None, max_length=1500)
    email: EmailStr | None = None
    is_activated: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=50)
    username: str | None = Field(default=None, min_length=8, max_length=1500)


class UsersTable(UserBase, table=True):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str
    username: str = Field(index=True)

