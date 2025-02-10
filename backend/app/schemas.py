from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class LoginForm(BaseModel):
    # Does it work well?
    email_username: (
        EmailStr
        | Annotated[str, StringConstraints(min_length=4, max_length=50)]
    )
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class AccessTokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)]
    email: EmailStr
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]


class UserResponse(UserBase):
    created_at: datetime
    is_activated: bool


class MultipleUsersResponse(BaseModel):
    count: int
    users: list[UserResponse]


class UserUpdate(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)] | None = None
    email: EmailStr | None = None
    is_activated: bool | None = None
    password: (
        Annotated[str, StringConstraints(min_length=8, max_length=50)] | None
    ) = None
    username: (
        Annotated[str, StringConstraints(min_length=4, max_length=50)] | None
    ) = None
