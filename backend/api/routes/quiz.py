"""Quiz mode routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import QuizRequest, QuizSubmitRequest, QuizResult
from services.quiz_service import quiz_service

router = APIRouter()


@router.post("/start")
async def start_quiz(request: QuizRequest, db: Session = Depends(get_db)):
    """Start a quiz session with generated questions (answers hidden)."""
    try:
        result = await quiz_service.create_quiz(
            request.document_id, db, request.topic, request.num_questions
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating quiz: {str(e)}")


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(request: QuizSubmitRequest):
    """Submit quiz answers and get scored results."""
    try:
        result = await quiz_service.score_quiz(request.quiz_id, request.answers)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring quiz: {str(e)}")
