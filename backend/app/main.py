"""FastAPI app entrypoint.

TODO:
  - Create the FastAPI() app instance.
  - Configure CORS to allow the Vite dev server origin (http://localhost:5173).
  - Include the upload, events, and auth routers.
  - On startup, call Base.metadata.create_all(engine) (or wire up Alembic).

Run with: uvicorn app.main:app --reload --port 8000
"""


from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  
from app.db import Base, engine
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Calendar PDF Sync", lifespan=lifespan)
app.include_router(auth.router)
