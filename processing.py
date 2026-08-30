import io
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from docx import Document
from zipfile import BadZipFile
from docx.opc.exceptions import PackageNotFoundError
from fastapi import HTTPException


def extract_text_from_pdf(change):
    page_list = []
    try:
        reader = PdfReader(io.BytesIO(change))
        for page in reader.pages:        
            text = page.extract_text()      
            page_list.append(text)
    except PdfReadError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file."
        )
    
    full_text = ",".join(page_list)
    return full_text


def extract_text_from_docx(contents):
    doc_list = []
    try:
        doc = Document(io.BytesIO(contents))

        for para in doc.paragraphs:
            text = para.text
            doc_list.append(text)
    except (PackageNotFoundError, BadZipFile):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted DOCX file."
        )
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