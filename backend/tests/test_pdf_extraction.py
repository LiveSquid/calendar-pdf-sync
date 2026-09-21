"""TODO: put 2-3 real sample PDFs in tests/fixtures/ (a course schedule,
a syllabus) and assert extract_text()/extract_tables() find known strings
(course codes, times, room numbers) in the output.
"""


from pathlib import Path
from app.services.pdf_extraction import extract_text, extract_tables

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_extract_text_finds_known_content():
    pdf_bytes = (FIXTURES_DIR / "EOSC211_2026_Schedule.pdf").read_bytes()
    text = extract_text(pdf_bytes)
    assert "Midterm" in text
    assert "Sep 10" in text


def test_extract_tables_returns_rows():
    pdf_bytes = (FIXTURES_DIR / "cpsc213_schedule_current.pdf").read_bytes()
    tables = extract_tables(pdf_bytes)
    assert len(tables) >= 1
    assert any("Sep 14-18" in str(cell) for row in tables[0] for cell in row)