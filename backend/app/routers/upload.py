"""POST /uploads, GET /uploads/{upload_id}"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Upload
from app.schemas import UploadOut
from app.services import llm_extraction
from app.services.event_mapper import events_from_llm_output
from app.services.pdf_extraction import PDFExtractionError, extract_tables, extract_text
from app.services.users import get_local_user

router = APIRouter(tags=["uploads"])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/uploads", response_model=UploadOut, status_code=201)
def upload_pdf(file: UploadFile, db: Session = Depends(get_db)):
    # Reading one byte past the limit tells us the file is too big without reading all of it.
    pdf_bytes = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(pdf_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF is too large (limit is 10 MB)")

    try:
        raw_text = extract_text(pdf_bytes)
        tables = extract_tables(pdf_bytes)
    except PDFExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    upload = Upload(
        user=get_local_user(db),
        filename=file.filename or "upload.pdf",
        raw_text=raw_text,
        status="extracted",
    )
    db.add(upload)

    try:
        llm_events = llm_extraction.extract_events(raw_text, tables)
        upload.events = events_from_llm_output(llm_events)
    except (llm_extraction.LLMExtractionError, ValueError) as e:
        # Keep the failed attempt (with its raw_text) so it can be inspected later.
        upload.status = "failed"
        upload.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=502, detail=f"Could not extract events: {e}")

    db.commit()
    return upload


@router.get("/uploads/{upload_id}", response_model=UploadOut)
def get_upload(upload_id: int, db: Session = Depends(get_db)):
    upload = db.get(Upload, upload_id)
    if upload is None or upload.user_id != get_local_user(db).id:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload
