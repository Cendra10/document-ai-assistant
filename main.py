from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    if file.content_type not in ("application/pdf", "text/plain", "application/json", "application/msword"):
        raise HTTPException(
            status_code=400, 
            detail="File type does not match."
            )
    return {"file name": file.filename, "file size": len(contents)}
