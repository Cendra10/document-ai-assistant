from pydantic import BaseModel

class UploadFileResponse(BaseModel):
    file_name: str
    file_size: int
    chunks: list[str]