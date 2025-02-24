from pydantic import BaseModel


class MetadataResponse(BaseModel):
    filename: str
    size: int
    content_type: str
    metadata: dict[str | int, str | int]
    hash: str
