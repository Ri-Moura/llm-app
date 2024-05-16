from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl

class QueryRequest(BaseModel):
    """
    QueryRequest represents the structure of a request to query an index.

    Attributes:
        question (str): The question to be queried.
        index_name (str): The name of the index to query.
    """
    question: str
    index_name: str

class EmbedStoreRequest(BaseModel):
    """
    EmbedStoreRequest represents the structure of a request to store an embedding.

    Attributes:
        url (str): The URL of the content to be embedded.
        index_name (str): The name of the index where the embedding will be stored.
    """
    url: str
    index_name: str

class BrandVoiceConfig(BaseModel):
    """
    BrandVoiceConfig represents the configuration for the brand voice, which includes either a URL or a file.

    Attributes:
        url (Optional[HttpUrl]): The URL of the brand voice configuration.
        file (Optional[UploadFile]): The file containing the brand voice configuration.
        index_name (str): The name of the index associated with the brand voice configuration.
    """
    url: Optional[HttpUrl] = None
    file: Optional[UploadFile] = None
    index_name: str
