"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Document schemas ---

class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_type: str
    file_size: int
    num_pages: int
    num_chunks: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Notes schemas ---

class NotesRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None
    question: Optional[str] = None


class NotesResponse(BaseModel):
    title: str
    content: str
    key_points: list[str]


# --- MCQ schemas ---

class MCQRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None
    num_questions: int = 5


class MCQOption(BaseModel):
    label: str
    text: str


class MCQQuestion(BaseModel):
    question: str
    options: list[MCQOption]
    correct_answer: str
    explanation: str


class MCQResponse(BaseModel):
    topic: str
    questions: list[MCQQuestion]


# --- Chat schemas ---

class ChatRequest(BaseModel):
    document_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


# --- Summary schemas ---

class SummaryRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None


class SummaryResponse(BaseModel):
    title: str
    summary: str
    key_concepts: list[str]


# --- Flashcard schemas ---

class FlashcardRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None
    num_cards: int = 10


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardResponse(BaseModel):
    topic: str
    cards: list[Flashcard]


# --- Quiz schemas ---

class QuizRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None
    num_questions: int = 10


class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: list[str]


class QuizResult(BaseModel):
    total_questions: int
    correct_answers: int
    score_percentage: float
    results: list[dict]


# --- Mind Map schemas ---

class MindMapRequest(BaseModel):
    document_id: int
    topic: Optional[str] = None


class MindMapResponse(BaseModel):
    mermaid_code: str
