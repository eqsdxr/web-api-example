from pydantic import BaseModel


class MetadataResponse(BaseModel):
    filename: str
    size: str
    filetype: str
    metadata: dict[str, str]
    hash: str
