from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl

class QueryRequest(BaseModel):
    question: str
    index_name: str

class EmbedStoreRequest(BaseModel):
    url: str
    index_name: str

class BrandVoiceConfig(BaseModel):
    url: Optional[HttpUrl] = None
    file: Optional[UploadFile] = None
    index_name: str
