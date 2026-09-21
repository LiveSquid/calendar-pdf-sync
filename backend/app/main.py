"""FastAPI app entrypoint.

TODO:
  - Create the FastAPI() app instance.
  - Configure CORS to allow the Vite dev server origin (http://localhost:5173).
  - Include the upload, events, and auth routers.
  - On startup, call Base.metadata.create_all(engine) (or wire up Alembic).

Run with: uvicorn app.main:app --reload --port 8000
"""
