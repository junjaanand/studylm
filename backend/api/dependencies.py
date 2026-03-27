"""Shared dependencies for API routes."""

from sqlalchemy.orm import Session
from models.database import SessionLocal


def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
