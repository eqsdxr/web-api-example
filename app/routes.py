from fastapi import APIRouter, UploadFile

from .models import MetadataResponse
from .extractor import extract_image_metadata

router = APIRouter()


@router.post("/upload", response_model=MetadataResponse)
async def upload_file(file: UploadFile):
    metadata = {}
    metadata["metadata"] = extract_image_metadata(file.file)
    metadata["filename"] = file.filename
    metadata["size"] = file.size
    metadata["content_type"] = file.content_type
    metadata["hash"] = file.__hash__()
    return MetadataResponse(**metadata)
