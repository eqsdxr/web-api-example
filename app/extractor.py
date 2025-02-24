from typing import BinaryIO
from PIL import Image
from PIL.ExifTags import TAGS
from fastapi import HTTPException, UploadFile
from asyncio import to_thread

from .config import logger


async def extract_image_metadata(img: BinaryIO) -> dict[str, str]:
    # Execute in a thread pool for performance reasons
    def _extract():
        metadata = {}
        try:
            with Image.open(img) as image:
                exifdata = image.getexif()
                for tag_id in exifdata:
                    tag_name = TAGS.get(tag_id, tag_id)
                    metadata[tag_name] = exifdata.get(tag_id)
        except Exception as e:
            logger.info(e)
            raise HTTPException(400, "Failed to process image")
        return metadata

    return await to_thread(_extract)


async def extract_metadata(file: UploadFile) -> dict[str, str]:
    match file.content_type:
        case "image/jpeg":
            return await extract_image_metadata(file.file)
    logger.info("Unsupported file type: ", file.content_type)
    raise HTTPException(415, "Unsupported file type")
