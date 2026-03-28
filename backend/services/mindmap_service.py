"""Service for generating Mermaid.js mind maps and flowcharts."""

from sqlalchemy.orm import Session
import re

from models.document import Document
from core.vectorstore import query_collection
from core.llm import get_llm
from prompts.mindmap_prompt import mindmap_prompt_template


class MindmapService:
    async def generate(self, document_id: int, db: Session, topic: str = None) -> str:
        """Generate Mermaid code based on document contents."""
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with ID {document_id} not found")

        # Define search query based on topic
        search_query = topic if topic else "Main concepts, definitions, hierarchies, and summary"

        # Get relevant chunks (k=10 for broad visual relationships)
        chunks = query_collection(doc.collection_name, search_query, k=10)
        if not chunks:
            raise ValueError("No context found in document to map.")

        context = "\n\n".join(chunks)

        # Build prompt and invoke LLM
        prompt = mindmap_prompt_template.format(context=context)
        llm = get_llm()
        response = await llm.ainvoke(prompt)

        text = response.content.strip()

        # Clean markdown if the LLM leaked it despite instructions
        if "```mermaid" in text:
            text = text.split("```mermaid")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        # Ensure it starts with graph TD
        if not text.startswith("graph"):
            text = "graph TD\n" + text

        return text


# Singleton
mindmap_service = MindmapService()
