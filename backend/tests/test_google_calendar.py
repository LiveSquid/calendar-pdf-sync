from app.services.google_calendar import build_event_body


def test_all_day_event_ends_the_next_day():
    body = build_event_body({"title": "Lab L1", "start_date": "2026-09-21", "date_is_approximate": False})
    assert body["start"] == {"date": "2026-09-21"}
    assert body["end"] == {"date": "2026-09-22"}


def test_approximate_date_is_noted_in_description():
    body = build_event_body({"title": "Lab L1", "start_date": "2026-09-21",
                             "date_is_approximate": True, "description": "Lab"})
    assert body["description"].startswith("Date approximate")
    assert body["description"].endswith("Lab")


def test_timed_event_defaults_to_one_hour():
    body = build_event_body({"title": "Lecture", "start_date": "2026-09-22",
                             "start_time": "14:00", "date_is_approximate": False})
    assert body["start"] == {"dateTime": "2026-09-22T14:00:00", "timeZone": "America/Vancouver"}
    assert body["end"] == {"dateTime": "2026-09-22T15:00:00", "timeZone": "America/Vancouver"}