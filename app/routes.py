from fastapi import APIRouter, Request, UploadFile, status

from app.config import logger
from app.models import MetadataResponseList
from app.utils import process_file

router = APIRouter()


@logger.catch  # Catch unexpected exceptions
@router.post(
    "/upload",
    response_model=MetadataResponseList,
    status_code=status.HTTP_200_OK,
    tags=["metadata"],
)
async def upload_files(
    files: list[UploadFile], request: Request
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
