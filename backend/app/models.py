"""SQLAlchemy ORM model."""

from datetime import date, datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    google_credentials_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    uploads: Mapped[list["Upload"]] = relationship(back_populates="user")


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str]
    raw_text: Mapped[str] = mapped_column(Text)
    status: Mapped[str]
    error_message: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="uploads")
    events: Mapped[list["ExtractedEvent"]] = relationship(
        back_populates="upload", cascade="all, delete-orphan"
    )


class ExtractedEvent(Base):
    __tablename__ = "extracted_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"))
    title: Mapped[str]
    start_date: Mapped[date]
    date_is_approximate: Mapped[bool]
    start_time: Mapped[str | None]
    end_time: Mapped[str | None]
    location: Mapped[str | None]
    description: Mapped[str | None] = mapped_column(Text)
    source_snippet: Mapped[str | None] = mapped_column(Text)
    included: Mapped[bool] = mapped_column(default=True)
    status: Mapped[str] = mapped_column(default="pending_review")
    google_event_id: Mapped[str | None]
    sync_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    upload: Mapped["Upload"] = relationship(back_populates="events")