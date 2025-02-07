from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


# User can use either email or username
class LoginForm(BaseModel):
    email: EmailStr | None
    username: Annotated[
        str | None, StringConstraints(min_length=4, max_length=50)
    ]
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    model_config = {"extra": "forbid"}


class LoginResponse(BaseModel):
    access_code: str


# Avoid using baseclasses for clarity


class UserCreate(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)]
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]
    model_config = {"extra": "forbid"}


class UserCreateResponse(BaseModel):
    email: EmailStr
    bio: Annotated[str, StringConstraints(max_length=500)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class UserDeleteResponse(BaseModel):
    email: EmailStr
    bio: Annotated[str, StringConstraints(max_length=500)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class SingleUserReadResponse(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)]
    created_at: datetime
    email: EmailStr
    is_activated: bool
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class MultipleUsersReadResponse(BaseModel):
    count: int
    users: list[SingleUserReadResponse]


class UserUpdate(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)]
    email: EmailStr
    is_activated: bool
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]
    model_config = {"extra": "forbid"}


class UserUpdateResponse(BaseModel):
    bio: Annotated[str, StringConstraints(max_length=500)]
    email: EmailStr
    is_activated: bool
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]
