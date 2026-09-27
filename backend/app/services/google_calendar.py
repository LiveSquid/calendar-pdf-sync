"""Google OAuth flow + Calendar API event insertion."""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauthlib.oauth2.rfc6749.errors import OAuth2Error

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
REDIRECT_URI = "http://localhost:8000/auth/google/callback"
CLIENT_SECRET_PATH = Path(__file__).resolve().parents[2] / "client_secret.json"
TIMEZONE = "America/Vancouver"

class GoogleCalendarError(Exception):
    """Raised when signing in to Google or creating a calendar event fails."""


def build_flow(code_verifier: str | None = None) -> Flow:
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_PATH,
        scopes = SCOPES,
        redirect_uri = REDIRECT_URI,
        code_verifier = code_verifier,
    )

def get_authorization_url() -> tuple[str, str, str]:
    flow = build_flow()
    url, state = flow.authorization_url(prompt = "consent")
    return url, state, flow.code_verifier


def exchange_code_for_credentials(code: str, code_verifier: str) -> Credentials:
    flow = build_flow(code_verifier=code_verifier)
    try:
        flow.fetch_token(code=code)
    except OAuth2Error as e:
        raise GoogleCalendarError(f"Could not finish Google sign-in: {e}") from e
    return flow.credentials


def load_credentials(credentials_json: str) -> Credentials:
    credentials = Credentials.from_authorized_user_info(json.loads(credentials_json), SCOPES)
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except RefreshError as e:
            raise GoogleCalendarError(
                "Google access expired or was revoked - reconnect your Google account"
            ) from e
    return credentials


def build_event_body(event: dict) -> dict:
    description = event.get("description") or ""
    if event["date_is_approximate"]:
        description = (
            "Date approximate: the PDF only gives the week, not the exact day.\n" + description
        ).strip()

    body = {"summary": event["title"], "description": description}

    if event.get("start_time"):
        start = datetime.strptime(f"{event['start_date']} {event['start_time']}", "%Y-%m-%d %H:%M")
        if event.get("end_time"):
            end = datetime.strptime(f"{event['start_date']} {event['end_time']}", "%Y-%m-%d %H:%M")
        else:
            end = start + timedelta(hours=1)
        body["start"] = {"dateTime": start.isoformat(), "timeZone": TIMEZONE}
        body["end"] = {"dateTime": end.isoformat(), "timeZone": TIMEZONE}
    else:
        start_day = date.fromisoformat(event["start_date"])
        body["start"] = {"date": start_day.isoformat()}
        body["end"] = {"date": (start_day + timedelta(days=1)).isoformat()}

    return body


def insert_event(credentials: Credentials, event: dict) -> str:
    service = build("calendar", "v3", credentials=credentials)
    try:
        created = service.events().insert(
            calendarId="primary", body=build_event_body(event)
        ).execute()
    except HttpError as e:
        raise GoogleCalendarError(f"Google Calendar rejected the event '{event['title']}': {e}") from e
    return created["id"]


