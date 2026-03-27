"""Application configuration loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """App-wide configuration settings."""

    # API Keys
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./data/chroma")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/studylm.db")

    # LLM settings
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "embed-english-v3.0"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    def ensure_directories(self):
        """Create required directories if they don't exist."""
        Path(self.CHROMA_PATH).mkdir(parents=True, exist_ok=True)
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path("./data").mkdir(parents=True, exist_ok=True)


settings = Settings()
