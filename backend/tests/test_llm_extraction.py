"""TODO: mock anthropic.Anthropic().messages.create (unittest.mock.patch) to
return a canned tool-use response (save one as
tests/fixtures/sample_claude_response.json) and assert extract_events()
parses it into the expected list of event dicts. Also test behavior on a
malformed/missing-field response.

Optional: gate a real live-API test behind an env var, e.g.
`if not os.environ.get("RUN_LIVE_LLM_TESTS"): pytest.skip(...)`.
"""
