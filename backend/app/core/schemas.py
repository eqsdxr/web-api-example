from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    bio: Annotated[str, StringConstraints(max_length=500)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(max_length=50)]


class UserResponse(BaseModel):
    email: EmailStr
    bio: Annotated[str, StringConstraints(max_length=500)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]


class UserUpdate(BaseModel):
    email: EmailStr
    bio: Annotated[str, StringConstraints(max_length=500)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=50)]
    username: Annotated[str, StringConstraints(min_length=4, max_length=50)]
