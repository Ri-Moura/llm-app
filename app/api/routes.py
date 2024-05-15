import time
import requests
import pdfplumber
from io import BytesIO
from typing import Dict, Optional
from pydantic import BaseModel, HttpUrl
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, UploadFile, File, Form

from app.utils.helper_functions import chunk_text, build_prompt
from app.services import openai_service, pinecone_service, scraping_service

app = FastAPI()

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

@app.post('/generate-content/')
async def generate_content(index_name: str = Form(...), url: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    """
    Generate content based on the brand voice extracted from the provided PDF URL or file.

    Args:
        index_name (str): The name of the Pinecone index.
        url (Optional[str]): The URL of the PDF file.
        file (Optional[UploadFile]): The PDF file uploaded by the user.

    Returns:
        dict: A dictionary containing the extracted brand voice.
    """
    try:
        if url:
            try:
                head_resp = requests.head(url)
                content_type = head_resp.headers['Content-Type']
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to retrieve URL: {str(e)}")

            if 'application/pdf' in content_type:
                url_text = scraping_service.extract_text_from_pdf(url)
            elif 'text/html' in content_type:
                url_text = scraping_service.scrape_website(url)
            else:
                raise HTTPException(status_code=400, detail="Unsupported URL content type")
        elif file:
            if file.content_type == 'application/pdf':
                content = await file.read()
                with pdfplumber.open(BytesIO(content)) as pdf:
                    url_text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
        else:
            raise HTTPException(status_code=400, detail="No input provided")

        chunks = chunk_text(url_text)
        pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, index_name)
        time.sleep(15)
        question_text = "What is the brand voice in this text?"
        context_chunks = pinecone_service.get_most_similar_chunks_for_query(question_text, index_name)
        prompt = build_prompt(question_text, context_chunks)
        answer = openai_service.get_llm_answer(prompt)

        return {"Brand Voice": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/handle-query/')
async def handle_query(query: QueryRequest):
    """
    Handle user queries related to the brand voice.

    Args:
        query (QueryRequest): The query request containing the question and index name.

    Returns:
        dict: A dictionary containing the question and the corresponding answer.
    """
    try:
        question_text = query.question
        context_chunks = pinecone_service.get_most_similar_chunks_for_query(question_text, query.index_name)
        prompt = build_prompt(question_text, context_chunks)
        answer = openai_service.get_llm_answer(prompt)

        return {"question": question_text, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/embed-and-store/')
async def embed_and_store(request: EmbedStoreRequest):
    """
    Embed and store text chunks from a provided URL into Pinecone.

    Args:
        request (EmbedStoreRequest): The request containing the URL and index name.

    Returns:
        JSONResponse: A JSON response indicating the success of the operation.
    """
    try:
        head_resp = requests.head(request.url)
        content_type = head_resp.headers['Content-Type']
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve URL: {str(e)}")

    if 'application/pdf' in content_type:
        url_text = scraping_service.extract_text_from_pdf(request.url)
    elif 'text/html' in content_type:
        url_text = scraping_service.scrape_website(request.url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported URL content type")

    chunks = chunk_text(url_text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, request.index_name)
    return JSONResponse({"message": "Chunks embedded and stored successfully"})

@app.post('/delete-index/')
async def delete_index(index_name: str):
    """
    Delete a specified index from Pinecone.

    Args:
        index_name (str): The name of the index to be deleted.

    Returns:
        JSONResponse: A JSON response indicating the success of the deletion.
    """
    pinecone_service.delete_index(index_name)
    return JSONResponse({"message": f"Index {index_name} deleted successfully"})
