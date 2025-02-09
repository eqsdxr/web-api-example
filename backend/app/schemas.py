from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class LoginForm(BaseModel):
    email: EmailStr | None
    username: Annotated[
        str | None, StringConstraints(min_length=4, max_length=50)
    ]
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    model_config = {"extra": "forbid"}


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


class UserUpdate(UserBase):
    is_activated: bool
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]

