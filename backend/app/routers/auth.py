"""GET /auth/google/login, GET /auth/google/callback, GET /auth/status

TODO:
  - GET /auth/google/login: build the authorization URL via
    google_calendar.build_flow() and redirect the browser to it.
  - GET /auth/google/callback?code=...: exchange the code for tokens via the
    same Flow, persist credentials.to_json() onto the user row, redirect
    back to the frontend.
  - GET /auth/status: return whether the user has valid stored credentials.
"""
