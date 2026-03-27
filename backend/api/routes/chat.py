"""Q&A Chat routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import ChatRequest, ChatResponse
from services.chat_service import chat_service

router = APIRouter()


@router.post("/ask", response_model=ChatResponse)
async def chat_ask(request: ChatRequest, db: Session = Depends(get_db)):
    """Ask a question and get an answer grounded in the document."""
    try:
        result = await chat_service.ask(request.document_id, request.question, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
