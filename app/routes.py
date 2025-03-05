from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, UploadFile, status
from fastapi.security import OAuth2PasswordRequestFormStrict

from app.config import get_settings, limiter, logger
from app.crud import authenticate
from app.deps import SessionDep, get_current_user
from app.models import MetadataResponseList, Token
from app.sec import create_access_token
from app.utils import process_file

router = APIRouter(prefix="/v1")


@logger.catch  # Catch unexpected exceptions
@router.post(
    "/upload",
    response_model=MetadataResponseList,
    status_code=status.HTTP_200_OK,
    tags=["metadata"],
    dependencies=[Depends(get_current_user)],
)
@limiter.limit("5/minute")
async def upload_files(
    files: list[UploadFile],
    # `request` is required by slowapi https://slowapi.readthedocs.io/en/latest/
    request: Request,
) -> MetadataResponseList:
    response = MetadataResponseList(count=len(files), metadata_set=[])
    for file in files:
        metadata = await process_file(file)
        if not request.client:
            host = "Unknown"
        else:
            host = request.client.host
        logger.info(f"{host}; {file.size}; {file.content_type}")
        response.metadata_set.append(metadata)
    return response


@logger.catch
@router.post(
    "/login/access-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    tags=["login"],
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
) -> Token:
    _ = request  # Stop showing the warning
    user = authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    access_token_expires = timedelta(
        minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
