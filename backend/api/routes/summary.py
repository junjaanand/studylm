"""Summary generation routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import SummaryRequest, SummaryResponse
from services.summary_service import summary_service

router = APIRouter()


@router.post("/generate", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    """Generate a summary of the document or a specific topic."""
    try:
        result = await summary_service.generate(
            request.document_id, db, request.topic
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
