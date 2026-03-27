"""Quiz mode service — Generate quizzes, manage sessions, and score answers."""

import json
import uuid
from core.llm import get_llm
from core.vectorstore import query_collection
from models.document import Document
from prompts.mcq_prompt import MCQ_PROMPT
from sqlalchemy.orm import Session


# In-memory quiz session storage
_quiz_sessions: dict = {}


class QuizService:
    """Handles quiz session creation, question generation, and scoring."""

    def _get_collection_name(self, document_id: int, db: Session) -> str:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document with id {document_id} not found")
        return doc.collection_name

    async def create_quiz(self, document_id: int, db: Session, topic: str = None, num_questions: int = 10) -> dict:
        """Generate a quiz with questions and store the session."""
        query = topic or "important concepts, facts, and definitions"
        collection_name = self._get_collection_name(document_id, db)
        chunks = query_collection(collection_name, query, k=8)
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant content found."

        llm = get_llm()
        prompt = MCQ_PROMPT.format(context=context, topic=query, num_questions=num_questions)
        response = await llm.ainvoke(prompt)

        from core.llm import clean_json_response
        try:
            result = json.loads(clean_json_response(response.content))
        except json.JSONDecodeError:
            raise ValueError("Failed to generate quiz questions. Please try again.")

        quiz_id = uuid.uuid4().hex[:16]
        _quiz_sessions[quiz_id] = {
            "quiz_id": quiz_id,
            "document_id": document_id,
            "topic": result.get("topic", topic or "General"),
            "questions": result.get("questions", []),
            "correct_answers": [q["correct_answer"] for q in result.get("questions", [])],
        }

        safe_questions = []
        for q in result.get("questions", []):
            safe_questions.append({"question": q["question"], "options": q["options"]})

        return {
            "quiz_id": quiz_id,
            "topic": result.get("topic", topic or "General"),
            "num_questions": len(safe_questions),
            "questions": safe_questions,
        }

    async def score_quiz(self, quiz_id: str, answers: list[str]) -> dict:
        """Score submitted quiz answers and return results."""
        session = _quiz_sessions.get(quiz_id)
        if not session:
            raise ValueError(f"Quiz session '{quiz_id}' not found or expired")

        questions = session["questions"]
        correct_answers = session["correct_answers"]
        total = len(questions)
        correct = 0
        results = []

        for i, q in enumerate(questions):
            student_answer = answers[i] if i < len(answers) else ""
            is_correct = student_answer.upper() == correct_answers[i].upper()
            if is_correct:
                correct += 1
            results.append({
                "question": q["question"],
                "your_answer": student_answer,
                "correct_answer": correct_answers[i],
                "is_correct": is_correct,
                "explanation": q.get("explanation", ""),
            })

        del _quiz_sessions[quiz_id]

        return {
            "total_questions": total,
            "correct_answers": correct,
            "score_percentage": round((correct / total) * 100, 1) if total > 0 else 0,
            "results": results,
        }


quiz_service = QuizService()
