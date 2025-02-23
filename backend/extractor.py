from typing import BinaryIO
from PIL import Image
from PIL.ExifTags import TAGS


def extract_image_metadata(img: BinaryIO) -> dict[str, str]:
    metadata = {}
    image = Image.open(img)
    exifdata = image.getexif()
    for tagid in exifdata:
        tagname = TAGS.get(tagid, tagid)
        value = exifdata.get(tagid)
        metadata[tagname] = value
    return metadata


