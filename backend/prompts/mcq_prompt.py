"""Prompt template for generating MCQs."""

MCQ_PROMPT = """You are a study assistant specializing in creating practice questions. Based on the following study material, generate {num_questions} multiple-choice questions.

**Study Material:**
{context}

**Topic Focus:** {topic}

For each question:
- Create a clear, unambiguous question
- Provide 4 options (A, B, C, D)
- Include the correct answer
- Add a brief explanation for why the answer is correct

Format your response as JSON:
{{
    "topic": "Topic name",
    "questions": [
        {{
            "question": "Question text",
            "options": [
                {{"label": "A", "text": "Option A text"}},
                {{"label": "B", "text": "Option B text"}},
                {{"label": "C", "text": "Option C text"}},
                {{"label": "D", "text": "Option D text"}}
            ],
            "correct_answer": "A",
            "explanation": "Why this answer is correct"
        }}
    ]
}}
"""
