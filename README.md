# AI File Knowledge API

## Description
Project API yang bisa menerima file (PDF, DOCX, TXT, JSON), mengekstrak isinya jadi teks bersih, lalu memecah (chunk) teks tersebut menjadi potongan-potongan yang siap digunakan untuk proses embedding/knowledge base.

## Features
- Upload file via endpoint `POST /uploadfile/`
- Dukung 4 tipe file: PDF, DOCX, TXT, JSON
- Validasi tipe file (whitelist content-type)
- Extract teks otomatis sesuai tipe file
- Chunking teks otomatis (ukuran & overlap bisa diatur)
- Validasi file kosong (ditolak)
- Validasi ukuran file maksimum 5 MB
- Error handling untuk file corrupt/rusak per tipe (PDF, DOCX, JSON, TXT)
- Response terstruktur (Pydantic model)

## Tech Stack
- FastAPI
- Pydantic
- pypdf
- python-docx

## Installation

1. Clone repository
   ```bash
   git clone https://github.com/Cendra10/document-ai-assistant.git
   cd document-ai-assistant
   ```

2. Buat virtual environment
   ```bash
   python -m venv .venv
   ```

3. Aktifkan virtual environment (Windows PowerShell)
   ```bash
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Jalankan aplikasi
   ```bash
   uvicorn main:app --reload
   ```

Server berjalan di `http://127.0.0.1:8000`

## Usage

1. Jalankan server (lihat langkah Installation), lalu buka Swagger UI di `http://127.0.0.1:8000/docs`
2. Pilih endpoint `POST /uploadfile/`
3. Klik "Try it out", upload file (PDF/DOCX/TXT/JSON, maksimal 5 MB)
4. Klik "Execute"

### Contoh request (curl)
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/uploadfile/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf;type=application/pdf'
```

### Contoh response (200 OK)
```json
{
  "file_name": "document.pdf",
  "file_size": 16656,
  "chunks": [
    "Ini adalah contoh potongan teks hasil chunking...",
    "..."
  ]
}
```

## Project Structure
```
document-ai-assistant/
   main.py              # Endpoint FastAPI
   schemas.py           # Pydantic response model
   processing.py        # Extract text (PDF/DOCX/TXT/JSON) & chunking
   requirements.txt     # Daftar dependencies
   README.md
```

## Future Improvement
- Tambah unit test otomatis (pytest)
- Dukungan tipe file lain (misal .md, .csv)
- Simpan hasil chunk ke database (persist), bukan cuma di response
- Rate limiting / auth untuk endpoint upload

## License
MIT License
