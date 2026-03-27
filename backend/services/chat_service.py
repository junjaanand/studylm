"""Chat Q&A service — RAG-based conversational answers."""

import json
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.chat_prompt import CHAT_PROMPT
from sqlalchemy.orm import Session


class ChatService:
    """Handles RAG-based conversational Q&A over documents."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def ask(self, document_id: int, question: str, db: Session) -> dict:
        """Retrieve relevant chunks and answer the question."""
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, question, k=5)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = CHAT_PROMPT.format(context=context, question=question)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            result = {
                "answer": response.content,
                "sources": [],
            }

        return result


chat_service = ChatService()
