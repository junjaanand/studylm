"""SQLAlchemy database engine and session setup."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables():
    """Create all database tables."""
    from models.document import Document  # noqa: F401
    Base.metadata.create_all(bind=engine)
