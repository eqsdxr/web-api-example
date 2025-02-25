from pydantic import BaseModel


class MetadataResponse(BaseModel):
    filename: str
    size: int
    content_type: str
    metadata: dict[str, str]
    hash: str


class MetadataResponseList(BaseModel):
    count: int
    metadata_set: list[MetadataResponse]
