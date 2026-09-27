"""Google sign-in routes: /auth/google/login, /auth/google/callback, and a temporary /auth/google/test-event."""

from datetime import date, timedelta

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.services import google_calendar

router = APIRouter(prefix="/auth/google", tags=["auth"])


# Temporary in-memory storage until the database exists.
LOCAL_USER = "local_user"
pending_logins: dict[str, str] = {}      # state -> code_verifier
stored_credentials: dict[str, str] = {}  # user -> credentials JSON


@router.get("/login")
def google_login():
    url, state, code_verifier = google_calendar.get_authorization_url()
    pending_logins[state] = code_verifier
    return RedirectResponse(url)


@router.get("/callback")
def google_callback(code: str | None = None, state: str | None = None, error: str | None = None):
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

    stored_credentials[LOCAL_USER] = credentials.to_json()
    return {"connected": True}


# Temporary: delete once POST /events/sync exists.
@router.post("/test-event")
def create_test_event():
    credentials_json = stored_credentials.get(LOCAL_USER)
    if credentials_json is None:
        raise HTTPException(status_code=401, detail="Not connected - visit /auth/google/login first")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    try:
        credentials = google_calendar.load_credentials(credentials_json)
        event_id = google_calendar.insert_event(credentials, {
            "title": "Calendar PDF Sync test event",
            "start_date": tomorrow,
            "date_is_approximate": False,
            "description": "Created by the calendar-pdf-sync standalone test. Safe to delete.",
        })
    except google_calendar.GoogleCalendarError as e:
        raise HTTPException(status_code=502, detail=str(e))

    stored_credentials[LOCAL_USER] = credentials.to_json()
    return {"google_event_id": event_id}