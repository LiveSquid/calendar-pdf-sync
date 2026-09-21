"""Maps between LLM-extracted event dicts, ExtractedEvent ORM rows, and
Google Calendar API event payloads.

TODO:
  def events_from_llm_output(upload_id: int, llm_events: list[dict]) -> list[ExtractedEvent]: ...
  def to_google_event_payload(event: ExtractedEvent) -> dict: ...
"""
