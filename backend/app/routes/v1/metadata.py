from fastapi import APIRouter, Depends, Request, UploadFile, status

from app.config import limiter, logger
from app.deps import get_current_user
from app.models import MetadataResponseList
from app.utils import get_file_info

metadata_router = APIRouter(prefix="/metadata", tags=["metadata"])


@logger.catch  # Catch unexpected exceptions
@metadata_router.post(
    "/extract",
    response_model=MetadataResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
@limiter.limit("5/minute")
async def upload_files(
    files: list[UploadFile],
    # `request` is required by slowapi https://slowapi.readthedocs.io/en/latest/
    request: Request,
) -> MetadataResponseList:
    # _ = request  # Stop showing the warning
    response = MetadataResponseList(count=len(files), metadata_set=[])
    for file in files:
        metadata = await get_file_info(file)
        if not request.client:
            host = "Unknown"
        else:
            host = request.client.host
        logger.info(f"{host}; {file.size}; {file.content_type}")
        response.metadata_set.append(metadata)
    return response
