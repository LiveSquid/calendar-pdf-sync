"""GET /events/preview (editing and syncing routes are added in step 6b)"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ExtractedEvent, Upload
from app.schemas import EventOut
from app.services.users import get_local_user

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/preview", response_model=list[EventOut])
def preview_events(upload_id: int, db: Session = Depends(get_db)):
    upload = db.get(Upload, upload_id)
    if upload is None or upload.user_id != get_local_user(db).id:
        raise HTTPException(status_code=404, detail="Upload not found")

    return db.scalars(
        select(ExtractedEvent)
        .where(ExtractedEvent.upload_id == upload_id)
        .order_by(ExtractedEvent.start_date, ExtractedEvent.id)
    ).all()
