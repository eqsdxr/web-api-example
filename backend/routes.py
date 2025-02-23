from fastapi import APIRouter, UploadFile

from .models import MetadataResponse

router = APIRouter()


@router.post("/upload")  # , response_model=MetadataResponse)
async def upload_file(file: UploadFile):
    return file.filename
