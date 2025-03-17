from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    subject: str | None = None


class UserBase(SQLModel):
    password: str = Field(min_length=8, max_length=50)


class UserPublic(SQLModel):
    id: UUID
    username: str


class UsersPublic(BaseModel):
    count: int
    users: list[UserPublic]


class UserIn(UserBase):
    username: str


class UserCreate(UserBase):
    username: str
    is_superuser: bool = False
    is_active: bool = True


class UserUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=5, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=255)
    is_superuser: bool | None = None
    is_active: bool | None = None


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, max_length=255)
    hashed_password: str
    is_superuser: bool
    is_active: bool
    items: list["Item"] = Relationship(
        back_populates="owner", cascade_delete=True
    )


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)


class ItemPublic(BaseModel):
    id: UUID
    title: str


class ItemsPublic(BaseModel):
    data: list[ItemPublic]


class Item(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: UUID = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")
