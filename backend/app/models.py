"""SQLAlchemy ORM models.

TODO: implement the following tables (see plan doc for full field list):

class User(Base):
    id, email, google_credentials_json (nullable text), created_at

class Upload(Base):
    id, user_id (FK -> users.id), filename, raw_text, status, error_message, created_at

class ExtractedEvent(Base):
    id, upload_id (FK -> uploads.id), title, start_date, start_time, end_time,
    location, description, source_snippet, included (bool, default True),
    status (pending_review|edited|synced|sync_failed), google_event_id,
    sync_error, created_at, updated_at

Keep `users` as a real table (even with a single row for now) rather than a
global singleton/token file -- this is what makes multi-user support additive
later instead of a rewrite.
"""
