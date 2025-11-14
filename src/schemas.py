from pydantic import BaseModel

class FileMetadata(BaseModel):
    channel_id: str
    type: str
    path: str
    name: str
    size: int
