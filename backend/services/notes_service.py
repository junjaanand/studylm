"""Notes generation service."""

import json
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.notes_prompt import NOTES_PROMPT
from sqlalchemy.orm import Session


class NotesService:
    """Generates structured notes from document content using RAG + LLM."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def generate(self, document_id: int, db: Session, topic: str = None, question: str = None) -> dict:
        """Retrieve relevant chunks and generate structured notes."""
        query = question or topic or "main concepts and key topics"
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, query, k=6)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = NOTES_PROMPT.format(context=context, query=query)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            result = {
                "title": topic or "Study Notes",
                "content": response.content,
                "key_points": [],
            }

        return result


notes_service = NotesService()
