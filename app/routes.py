from os import SEEK_END

from fastapi import APIRouter, Request, UploadFile, status

from .models import MetadataResponse
from .extractor import extract_metadata
from .config import logger
from .utils import calculate_sha256

router = APIRouter()


@logger.catch  # Catch unexpected exceptions
@router.post(
    "/upload",
    response_model=MetadataResponse,
    status_code=status.HTTP_200_OK,
    tags=["metadata"],
)
async def upload_file(file: UploadFile, request: Request) -> MetadataResponse:
    file_size = file.file.seek(0, SEEK_END)
    await file.seek(0)  # Reset pointer position
    metadata = {
        "filename": file.filename,
        "size": file_size,
        "content_type": file.content_type,
        "metadata": await extract_metadata(file),
        "hash": await calculate_sha256(file),
    }
    if not request.client:
        host = "Unknown"
    else:
        host = request.client.host
    logger.info(f"{host}; {file_size}; {file.filename}; {file.content_type}")
    return MetadataResponse(**metadata)
