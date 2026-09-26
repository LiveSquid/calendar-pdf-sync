"""TODO: mock anthropic.Anthropic().messages.create (unittest.mock.patch) to
return a canned tool-use response (save one as
tests/fixtures/sample_claude_response.json) and assert extract_events()
parses it into the expected list of event dicts. Also test behavior on a
malformed/missing-field response.

Optional: gate a real live-API test behind an env var, e.g.
`if not os.environ.get("RUN_LIVE_LLM_TESTS"): pytest.skip(...)`.
"""

from unittest.mock import patch, MagicMock
from app.services.llm_extraction import extract_events, ExtractedEvents, ExtractedEvent


from unittest.mock import patch, MagicMock
import pytest
from app.services.llm_extraction import (
    extract_events, format_tables, ExtractedEvents, ExtractedEvent, LLMExtractionError,
)


def test_extract_events_parses_response():
    fake_response = MagicMock()
    fake_response.parsed_output = ExtractedEvents(events=[
        ExtractedEvent(title="Midterm 1", start_date="2026-10-08", date_is_approximate=False,
                       source_snippet="Oct 08 Midterm 1"),
    ])

    with patch("app.services.llm_extraction.anthropic.Anthropic") as mock_client_cls:
        mock_client_cls.return_value.messages.parse.return_value = fake_response
        events = extract_events("...some raw text...", [])

    assert events == [{
        "title": "Midterm 1", "start_date": "2026-10-08", "date_is_approximate": False,
        "start_time": None, "end_time": None, "location": None, "description": None,
        "source_snippet": "Oct 08 Midterm 1",
    }]


def test_extract_events_raises_when_response_unparseable():
    fake_response = MagicMock()
    fake_response.parsed_output = None
    fake_response.stop_reason = "max_tokens"

    with patch("app.services.llm_extraction.anthropic.Anthropic") as mock_client_cls:
        mock_client_cls.return_value.messages.parse.return_value = fake_response
        with pytest.raises(LLMExtractionError, match="max_tokens"):
            extract_events("...some raw text...", [])


def test_format_tables_joins_cells_and_cleans_them():
    tables = [[["0", "Sep 7-11", None, "1a: Memory &\nNumbers"]]]
    assert format_tables(tables) == "Table 1:\n0 | Sep 7-11 |  | 1a: Memory & Numbers"