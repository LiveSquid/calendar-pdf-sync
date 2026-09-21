"""GET /events/preview, PATCH /events/{id}, PUT /events/batch, POST /events/sync

TODO:
  - GET /events/preview?upload_id=...: list ExtractedEvent rows for an upload.
  - PATCH /events/{event_id}: partial update, set status="edited".
  - PUT /events/batch: apply a list of partial updates in one call.
  - POST /events/sync: for each included event_id, get_credentials(user),
    google_calendar.insert_event(...), set status to "synced" or
    "sync_failed" + sync_error, return per-event results.
"""
