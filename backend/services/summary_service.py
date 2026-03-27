"""Summary generation service."""

import json
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.summary_prompt import SUMMARY_PROMPT
from sqlalchemy.orm import Session


class SummaryService:
    """Generates document or topic summaries using RAG + LLM."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def generate(self, document_id: int, db: Session, topic: str = None) -> dict:
        """Retrieve relevant chunks and generate a structured summary."""
        query = topic or "complete overview and main topics"
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, query, k=8)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = SUMMARY_PROMPT.format(context=context, topic=query)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            result = {"title": topic or "Document Summary", "summary": response.content, "key_concepts": []}

        return result


summary_service = SummaryService()
