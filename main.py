from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
from docx import Document
import io
import json
from pydantic import BaseModel

app = FastAPI()

class UploadFileResponse(BaseModel):
    file_name: str
    file_size: int
    chunks: list[str]

@app.post("/uploadfile/", response_model=UploadFileResponse)
async def create_upload_file(file: UploadFile):

    contents = await file.read() 

    if file.content_type not in ("application/pdf", "text/plain", "application/json", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        raise HTTPException(
            status_code=400, 
            detail="File type does not match."
            )
    elif file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(contents)
    
    elif file.content_type == "text/plain":
        extracted_text = contents.decode('utf-8')
    
    elif file.content_type == "application/json":
        extracted_text = json.loads(contents.decode('utf-8'))

    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_text = extract_text_from_docx(contents)

    if isinstance(extracted_text, dict):
        extracted_text = json.dumps(extracted_text)

    chunks = chunk_text(extracted_text)

    return {"file_name": file.filename, "file_size": len(contents), "chunks": chunks}

def extract_text_from_pdf(change):
    page_list = []
    reader = PdfReader(io.BytesIO(change))
    
    for page in reader.pages:        
        text = page.extract_text()      
        page_list.append(text)
    full_text = ",".join(page_list)
    return full_text

def extract_text_from_docx(contents):
    doc_list = []
    doc = Document(io.BytesIO(contents))

    for para in doc.paragraphs:
        text = para.text
        doc_list.append(text)
    full_text = ",".join(doc_list)
    return full_text

def chunk_text(text, chunk_size=500, overlap=100):
    result = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        result.append(chunk)

        start = end - overlap 
    return result