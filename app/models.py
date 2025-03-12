from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class MetadataResponse(BaseModel):
    filename: str
    size: int
    content_type: str
    metadata: dict[int | str, int | str]
    hash: str


class MetadataResponseList(BaseModel):
    count: int
    metadata_set: list[MetadataResponse]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    subject: str | None = None


class UserBase(SQLModel):
    password: str = Field(min_length=8, max_length=50)


class UserResponse(SQLModel):
    id: UUID
    username: str


class UsersPublic(BaseModel):
    count: int
    users: list[UserResponse]


class UserIn(UserBase):
    username: str


class UserCreate(UserBase):
    username: str
    is_superuser: bool = False
    is_active: bool = True


class UserUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=5, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=50)
    is_superuser: bool | None = None
    is_active: bool | None = None


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    is_superuser: bool
    is_active: bool
