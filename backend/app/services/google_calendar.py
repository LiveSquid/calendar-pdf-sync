"""Google OAuth flow + Calendar API event insertion.

TODO:
  - def build_flow() -> google_auth_oauthlib.flow.Flow:
      Load client_secret.json, scopes=["https://www.googleapis.com/auth/calendar.events"],
      redirect_uri pointing at this app's own /auth/google/callback route
      (NOT InstalledAppFlow.run_local_server() -- the flow should terminate
      at a backend route so a future multi-user version can reuse it).
  - def get_credentials(user) -> google.oauth2.credentials.Credentials:
      Load from user.google_credentials_json, refresh via Request() if
      credentials.expired, and persist the refreshed JSON back onto the user.
  - def insert_event(credentials, event: ExtractedEvent) -> str:
      Build the Calendar API event payload from an ExtractedEvent row, call
      events().insert(calendarId="primary", body=...).execute(), and return
      the created event's id.
"""
