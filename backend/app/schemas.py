"""Pydantic request/response models for the API.

TODO: define schemas mirroring models.py, e.g.:
  - EventOut (id, title, start_date, start_time, end_time, location,
    description, included, status, source_snippet)
  - EventUpdate (all fields optional, for PATCH /events/{id})
  - EventBatchUpdate (list of partial updates, for PUT /events/batch)
  - SyncRequest (event_ids: list[int])
  - SyncResult (id, status, google_event_id | error)
  - UploadOut (id, filename, status, error_message)
  - AuthStatus (connected: bool, email: str | None)

These double as the source of truth for the frontend's TypeScript types in
frontend/src/types.ts -- keep them in sync by hand for now.
"""
