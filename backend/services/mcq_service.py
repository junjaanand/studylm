"""MCQ generation service."""

import json
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.mcq_prompt import MCQ_PROMPT
from sqlalchemy.orm import Session


class MCQService:
    """Generates multiple-choice questions from document content using RAG + LLM."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def generate(self, document_id: int, db: Session, topic: str = None, num_questions: int = 5) -> dict:
        """Retrieve relevant chunks and generate MCQs with answers and explanations."""
        query = topic or "important concepts and facts"
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, query, k=6)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = MCQ_PROMPT.format(context=context, topic=query, num_questions=num_questions)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            result = {"topic": topic or "General", "questions": []}

        return result


mcq_service = MCQService()
