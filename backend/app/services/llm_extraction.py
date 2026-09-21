"""Calls the Claude API with forced tool-use to extract structured events
from raw PDF text.

TODO:
  - Define the `record_events` tool: an input JSON schema describing an
    `events` array, each item with title, start_date, start_time (nullable),
    end_time (nullable), location (nullable), description (nullable),
    source_snippet (nullable).
  - def extract_events(raw_text: str) -> list[dict]:
      Call anthropic.Anthropic().messages.create(..., tools=[record_events_tool],
      tool_choice={"type": "tool", "name": "record_events"}), then parse the
      tool_use content block's `input` field.
  - Handle malformed/missing responses gracefully (raise a clear exception
    the router can turn into a useful error, rather than letting a KeyError
    bubble up).

See the `claude-api` skill / current Anthropic docs for the current model ID
and the exact tool-use message shape before implementing.
"""
