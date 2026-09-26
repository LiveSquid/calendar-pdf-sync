# Extracts raw text (and tables) from a PDF file using pdfplumber.

import io 
import pdfplumber

def extract_text(pdf_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page_texts = []
        for page in pdf.pages:
            text = page.extract_text()
            if text is None:
                text = ""
            page_texts.append(text)
    return "\n\n".join(page_texts)


def extract_tables(pdf_bytes: bytes) -> list[list[list[str | None]]]:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        tables: list[list[list[str | None]]] = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables



