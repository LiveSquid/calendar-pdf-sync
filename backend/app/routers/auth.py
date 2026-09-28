"""Google sign-in routes: /auth/google/login, /auth/google/callback, and a temporary /auth/google/test-event."""

from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.services import google_calendar
from app.db import get_db
from app.services.users import get_local_user

router = APIRouter(prefix="/auth/google", tags=["auth"])

pending_logins: dict[str, str] = {}      # state -> code_verifier


@router.get("/login")
def google_login():
    url, state, code_verifier = google_calendar.get_authorization_url()
    pending_logins[state] = code_verifier
    return RedirectResponse(url)


@router.get("/callback")
def google_callback(  
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):

    if error:
        raise HTTPException(status_code=400, detail=f"Google sign-in was cancelled or failed: {error}")

    code_verifier = pending_logins.pop(state, None)
    if code is None or code_verifier is None:
        raise HTTPException(
            status_code=400,
            detail="Unknown or expired sign-in attempt - start again at /auth/google/login",
        )

    try:
        credentials = google_calendar.exchange_code_for_credentials(code, code_verifier)
    except google_calendar.GoogleCalendarError as e:
        raise HTTPException(status_code=502, detail=str(e))

    user = get_local_user(db)
    user.google_credentials_json = credentials.to_json()
    db.commit()
    return {"connected": True}


@router.get("/status")
def google_status(db: Session = Depends(get_db)):
    user = get_local_user(db)
    return {"connected": user.google_credentials_json is not None}


# Temporary: delete once POST /events/sync exists.
@router.post("/test-event")
def create_test_event(db: Session = Depends(get_db)):
    user = get_local_user(db)
    if user.google_credentials_json is None:
        raise HTTPException(status_code=401, detail="Not connected - visit /auth/google/login first")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    try:
        credentials = google_calendar.load_credentials(user.google_credentials_json)
        event_id = google_calendar.insert_event(credentials, {
            "title": "Calendar PDF Sync test event",
            "start_date": tomorrow,
            "date_is_approximate": False,
            "description": "Created by the calendar-pdf-sync standalone test. Safe to delete.",
        })
    except google_calendar.GoogleCalendarError as e:
        raise HTTPException(status_code=502, detail=str(e))

    user.google_credentials_json = credentials.to_json()
    db.commit()
    return {"google_event_id": event_id}