from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
import io

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    contents = await file.read()

    if file.content_type not in ("application/pdf", "text/plain", "application/json", "application/msword"):
        raise HTTPException(
            status_code=400, 
            detail="File type does not match."
            )
    if file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(contents)
        return {"file name": file.filename, "file size": len(contents), "file extracted text": extracted_text}
    else:
        return {"file name": file.filename, "file size": len(contents)}

def extract_text_from_pdf(contents):
    page_list = []
    reader = PdfReader(io.BytesIO(contents))
    
    for page in reader.pages:        
        text = page.extract_text()      
        page_list.append(text)
    full_text = ",".join(page_list)
    return full_text