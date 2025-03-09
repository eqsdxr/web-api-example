from fastapi import APIRouter, Depends, Request, status

from app.config import limiter, logger
from app.deps import CurrentUser, get_current_user
from app.models import UserResponse

user_router = APIRouter(prefix="/users", tags=["user"])


@logger.catch  # Catch unexpected exceptions
@user_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
@limiter.limit("5/minute")
async def get_user_me(
    current_user: CurrentUser,
    request: Request,
) -> UserResponse:
    _ = request
    return UserResponse(**current_user.model_dump())
