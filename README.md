# AI File Knowledge API

## Description
An API that accepts files (PDF, DOCX, TXT, JSON), extracts their content into clean text, then splits (chunks) the text into pieces ready for further processing (e.g. embedding/knowledge base).

## Features
- Upload files via `POST /uploadfile/` endpoint
- Supports 4 file types: PDF, DOCX, TXT, JSON
- File type validation (content-type whitelist)
- Automatic text extraction per file type
- Automatic text chunking (configurable size & overlap)
- Empty file validation (rejected)
- Maximum file size validation (5 MB)
- Error handling for corrupted/invalid files per type (PDF, DOCX, JSON, TXT)
- Structured response (Pydantic model)

## Tech Stack
- FastAPI
- Pydantic
- pypdf
- python-docx

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Cendra10/document-ai-assistant.git
   cd document-ai-assistant
   ```

2. Create a virtual environment
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment (Windows PowerShell)
   ```bash
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application
   ```bash
   uvicorn main:app --reload
   ```

The server runs at `http://127.0.0.1:8000`

## Usage

1. Start the server (see Installation steps), then open Swagger UI at `http://127.0.0.1:8000/docs`
2. Select the `POST /uploadfile/` endpoint
3. Click "Try it out", upload a file (PDF/DOCX/TXT/JSON, max 5 MB)
4. Click "Execute"

### Example request (curl)
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/uploadfile/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf;type=application/pdf'
```

### Example response (200 OK)
```json
{
  "file_name": "document.pdf",
  "file_size": 16656,
  "chunks": [
    "This is an example text chunk from the chunking result...",
    "..."
  ]
}
```

## Project Structure
```
document-ai-assistant/
   main.py              # FastAPI endpoint
   schemas.py           # Pydantic response model
   processing.py        # Text extraction (PDF/DOCX/TXT/JSON) & chunking
   requirements.txt     # Dependency list
   README.md
```

## Future Improvement
- Add automated unit tests (pytest)
- Support for additional file types (e.g. .md, .csv)
- Persist chunk results to a database instead of only returning them in the response
- Rate limiting / authentication for the upload endpoint

## License
MIT License
