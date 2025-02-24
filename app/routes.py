from os import SEEK_END

from fastapi import APIRouter, UploadFile

from .models import MetadataResponse
from .extractor import extract_metadata
from .config import logger
from .utils import calculate_sha256

router = APIRouter()


@logger.catch  # Catch unexpected exceptions
@router.post("/upload", response_model=MetadataResponse)
async def upload_file(file: UploadFile) -> MetadataResponse:
    file_size = file.file.seek(0, SEEK_END)
    await file.seek(0)  # Reset pointer position
    metadata = {
        "filename": file.filename,
        "size": file_size,
        "content_type": file.content_type,
        "metadata": await extract_metadata(file),
        "hash": await calculate_sha256(file),
    }
    return MetadataResponse(**metadata)
