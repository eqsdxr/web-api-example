from typing import BinaryIO
from PIL import Image
from PIL.ExifTags import TAGS
from fastapi import HTTPException, UploadFile


async def extract_image_metadata(img: BinaryIO) -> dict[str, str]:
    metadata = {}
    try:
        with Image.open(img) as image:
            exifdata = image.getexif()
            for tag_id in exifdata:
                tag_name = TAGS.get(tag_id, tag_id)
                metadata[tag_name] = exifdata.get(tag_id)
    except Exception:
        raise HTTPException(400, "Failed to process image")
    return metadata


async def extract_metadata(file: UploadFile) -> dict[str, str]:
    match file.content_type:
        case "image/jpeg":
            return await extract_image_metadata(file.file)
    raise HTTPException(415, "Unsupported file type")
