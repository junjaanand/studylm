"""Flashcard generation service."""

import json
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.flashcard_prompt import FLASHCARD_PROMPT
from sqlalchemy.orm import Session


class FlashcardService:
    """Generates flashcards from document content using RAG + LLM."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def generate(self, document_id: int, db: Session, topic: str = None, num_cards: int = 10) -> dict:
        """Retrieve relevant chunks and generate flashcards."""
        query = topic or "key terms, definitions, and concepts"
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, query, k=6)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = FLASHCARD_PROMPT.format(context=context, topic=query, num_cards=num_cards)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            result = {"topic": topic or "General", "cards": []}

        return result


flashcard_service = FlashcardService()
