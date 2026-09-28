"""FastAPI app entry point.

Run from backend/ with: uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401 - importing registers the tables on Base
from app.db import Base, engine
from app.routers import auth, events, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Calendar PDF Sync", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(events.router)
