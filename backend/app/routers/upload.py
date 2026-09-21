"""POST /upload, GET /uploads/{upload_id}

TODO:
  - POST /upload: accept multipart PDF, run pdf_extraction.extract_text(),
    save an Upload row, run llm_extraction.extract_events() on the text,
    map results to ExtractedEvent rows via event_mapper, return
    { upload_id, status }.
  - GET /uploads/{upload_id}: return the Upload's status/error_message.
  - Keep this endpoint synchronous (no background task queue needed at this
    scope) -- see plan doc.
"""
