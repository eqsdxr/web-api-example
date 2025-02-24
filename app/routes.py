from fastapi import APIRouter, UploadFile

from .models import MetadataResponse
from .extractor import extract_metadata
from .config import logger

router = APIRouter()


@logger.catch  # Catch unexpected exceptions
@router.post("/upload", response_model=MetadataResponse)
async def upload_file(file: UploadFile) -> MetadataResponse:
    metadata = {}
    metadata["filename"] = file.filename
    metadata["size"] = file.size
    metadata["content_type"] = file.content_type
    metadata["metadata"] = await extract_metadata(file)
    metadata["hash"] = file.__hash__()
    return MetadataResponse(**metadata)
