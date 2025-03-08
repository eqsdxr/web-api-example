from asyncio import to_thread
from hashlib import sha256
from os import SEEK_END
from typing import BinaryIO

from fastapi import HTTPException, UploadFile, status
from PIL import Image
from PIL.ExifTags import TAGS

from app.config import logger
from app.models import MetadataResponse


async def parse_image_metadata(img: BinaryIO) -> dict[str, str]:
    # Execute in a thread pool for performance reasons
    def _extract():
        img.seek(0)  # Ensure the file pointer is in the start
        metadata = {}
        try:
            with Image.open(img) as image:
                exifdata = image.getexif()
                for tag_id in exifdata:
                    tag_name = TAGS.get(tag_id, tag_id)
                    metadata[tag_name] = exifdata.get(tag_id)
        except Exception as e:
            logger.info(e)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to process image"
            )
        return metadata

    return await to_thread(_extract)


async def extract_metadata(file: UploadFile) -> dict[str, str]:
    match file.content_type:
        case "image/jpeg" | "image/png":
            return await parse_image_metadata(file.file)
        case _:
            logger.info("Unsupported file type: ", file.content_type)
            raise HTTPException(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "Unsupported media type",
            )


async def calculate_sha256(file: UploadFile) -> str:
    hasher = sha256()
    await file.seek(0)  # Start in the beginning
    while chunk := await file.read(8192):
        hasher.update(chunk)
    await file.seek(0)  # Reset pointer position
    return hasher.hexdigest()


async def get_file_info(file: UploadFile) -> MetadataResponse:
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
