"""MCQ generation routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import MCQRequest, MCQResponse
from services.mcq_service import mcq_service

router = APIRouter()


@router.post("/generate", response_model=MCQResponse)
async def generate_mcqs(request: MCQRequest, db: Session = Depends(get_db)):
    """Generate multiple-choice questions from a document."""
    try:
        result = await mcq_service.generate(
            request.document_id, db, request.topic, request.num_questions
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating MCQs: {str(e)}")
