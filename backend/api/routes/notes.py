"""Notes generation routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import NotesRequest, NotesResponse
from services.notes_service import notes_service

router = APIRouter()


@router.post("/generate", response_model=NotesResponse)
async def generate_notes(request: NotesRequest, db: Session = Depends(get_db)):
    """Generate structured notes from a document based on a topic or question."""
    try:
        result = await notes_service.generate(
            request.document_id, db, request.topic, request.question
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating notes: {str(e)}")
