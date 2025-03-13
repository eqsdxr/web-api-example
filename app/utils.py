from hashlib import sha256

from fastapi import UploadFile


async def calculate_sha256(file: UploadFile) -> str:
    hasher = sha256()
    await file.seek(0)  # Start in the beginning
    while chunk := await file.read(8192):
        hasher.update(chunk)
    await file.seek(0)  # Reset pointer position
    return hasher.hexdigest()
