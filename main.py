from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
from docx import Document
import io
import json

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    contents = await file.read() 

    if file.content_type not in ("application/pdf", "text/plain", "application/json", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        raise HTTPException(
            status_code=400, 
            detail="File type does not match."
            )
    elif file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(contents)
        return {"file name": file.filename, "file size": len(contents), "file extracted text": extracted_text}
    
    elif file.content_type == "text/plain":
        extracted_text = contents.decode('utf-8')
        return{"file name": file.filename, "file size": len(contents), "file extracted text": extracted_text}
    
    elif file.content_type == "application/json":
        extracted_text = json.loads(contents.decode('utf-8'))
        return{"file name": file.filename, "file size": len(contents), "file extracted text": extracted_text}

    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_text = extract_text_from_docx(contents)
        return {"file name": file.filename, "file size": len(contents), "file extracted text": extracted_text}

    else:
        return {"file name": file.filename, "file size": len(contents)}

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