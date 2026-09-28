"""Converts Claude's extracted event dicts into ExtractedEvent database rows."""

from datetime import date

from app.models import ExtractedEvent


def events_from_llm_output(llm_events: list[dict]) -> list[ExtractedEvent]:
    return [
        ExtractedEvent(
            title=event["title"],
            start_date=date.fromisoformat(event["start_date"]),
            date_is_approximate=event["date_is_approximate"],
            start_time=event["start_time"],
            end_time=event["end_time"],
            location=event["location"],
            description=event["description"],
            source_snippet=event["source_snippet"],
        )
        for event in llm_events
    ]
