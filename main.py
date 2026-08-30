from fastapi import FastAPI, File, UploadFile, HTTPException
import json

from schemas import UploadFileResponse
from processing import extract_text_from_pdf, extract_text_from_docx, chunk_text

app = FastAPI()


@app.post("/uploadfile/", response_model=UploadFileResponse)
async def create_upload_file(file: UploadFile):

    contents = await file.read()
    size = len(contents)
    file.file.seek(0)

    if size == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty."
        )
    if size > 5*1024*1024:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 5 MB."
        )

    if file.content_type not in ("application/pdf", "text/plain", "application/json", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
        raise HTTPException(
            status_code=400, 
            detail="File type does not match."
            )

    elif file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(contents)
    
    elif file.content_type == "text/plain":
        try:
            extracted_text = contents.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted Text Document file."
        )

    elif file.content_type == "application/json":
        try:
            extracted_text = json.loads(contents.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted JSON file."
        )

    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(contents)


    if isinstance(extracted_text, dict):
        extracted_text = json.dumps(extracted_text)

    chunks = chunk_text(extracted_text)

    return {"file_name": file.filename, "file_size": len(contents), "chunks": chunks}