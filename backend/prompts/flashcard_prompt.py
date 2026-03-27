"""Prompt template for flashcard generation."""

FLASHCARD_PROMPT = """You are a study assistant. Based on the following study material, generate {num_cards} flashcards for effective revision.

**Study Material:**
{context}

**Topic Focus:** {topic}

Create flashcards with:
- Front: A question, term, or concept
- Back: The answer, definition, or explanation

Format your response as JSON:
{{
    "topic": "Topic name",
    "cards": [
        {{
            "front": "Question or term",
            "back": "Answer or definition"
        }}
    ]
}}
"""
