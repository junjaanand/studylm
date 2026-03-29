"""API Routes for Mind Map and Flowchart Generation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.schemas import MindMapRequest, MindMapResponse
from services.mindmap_service import mindmap_service

router = APIRouter()

@router.post("/generate", response_model=MindMapResponse)
async def generate_mindmap(request: MindMapRequest, db: Session = Depends(get_db)):
    """Generate a Mermaid.js mind map flowchart from document chunks."""
    try:
        mermaid_code = await mindmap_service.generate(
            document_id=request.document_id,
            db=db,
            topic=request.topic
        )
        return MindMapResponse(mermaid_code=mermaid_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate mind map: {e}")
