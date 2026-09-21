"""Extracts raw text (and tables) from a PDF file using pdfplumber.

TODO:
  def extract_text(pdf_bytes: bytes) -> str: ...
  def extract_tables(pdf_bytes: bytes) -> list[list[list[str]]]: ...

Keep this module's public interface small and stable (just these two
functions) so the underlying library (pdfplumber vs PyMuPDF) can be swapped
later without touching callers.
"""

import io 
import pdfplumber