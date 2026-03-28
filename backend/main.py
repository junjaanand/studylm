"""StudyLM Backend — FastAPI Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import documents, notes, mcq, chat, summary, flashcards, quiz, mindmap
from core.config import settings
from models.database import create_tables

app = FastAPI(
    title="StudyLM API",
    description="AI-powered student study assistant",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel production URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(mcq.router, prefix="/api/mcq", tags=["MCQ"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(summary.router, prefix="/api/summary", tags=["Summary"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["Flashcards"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(mindmap.router, prefix="/api/mindmap", tags=["MindMap"])


@app.on_event("startup")
async def startup():
    """Initialize database and required directories on startup."""
    settings.ensure_directories()
    create_tables()


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "StudyLM"}
