"""Flashcard generation routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import FlashcardRequest, FlashcardResponse
from services.flashcard_service import flashcard_service

router = APIRouter()


@router.post("/generate", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest, db: Session = Depends(get_db)):
    """Generate flashcards from a document."""
    try:
        result = await flashcard_service.generate(
            request.document_id, db, request.topic, request.num_cards
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating flashcards: {str(e)}")
