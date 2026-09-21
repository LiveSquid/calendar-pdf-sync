# Calendar PDF Sync

Upload a calendar PDF (course schedule, syllabus, event list), review the events an LLM extracts from it, then sync the ones you keep into Google Calendar.

See [`.claude/plans`](.) design plan (or ask for a copy) for the full architecture write-up: data flow, API design, data model, and build order.

## Status

Scaffolding only — core logic (PDF extraction, Claude tool-use extraction, Google OAuth + Calendar insert, API routes, frontend UI) is still TODO. See `TODO` docstrings in `backend/app/**` and the Build Order section of the design plan for the recommended sequence.

## Setup (once implemented)

1. `cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in `ANTHROPIC_API_KEY`.
3. Set up a Google Cloud project (Calendar API enabled, OAuth consent screen in Testing mode, yourself as a test user), download OAuth client credentials as `backend/client_secret.json` (see `backend/client_secret.example.json` for the expected shape).
4. `uvicorn app.main:app --reload --port 8000` (from `backend/`)
5. `cd frontend && npm install && npm run dev`

## Design Decisions

(Fill in once built: why pdfplumber vs PyMuPDF, why tool-use over free-text parsing, why SQLite now / Postgres later, etc. — see the design plan for the reasoning to summarize here.)
