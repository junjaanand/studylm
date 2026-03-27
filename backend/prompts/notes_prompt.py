"""Prompt template for generating structured notes."""

NOTES_PROMPT = """You are a helpful study assistant. Based on the following study material, generate well-structured notes.

**Study Material:**
{context}

**Student's Question/Topic:** {query}

Generate detailed, well-organized notes with:
1. A clear title
2. Key concepts explained simply
3. Important definitions
4. Examples where relevant
5. A list of key points to remember

Format your response as JSON:
{{
    "title": "Notes title",
    "content": "Full notes in markdown format",
    "key_points": ["point 1", "point 2", ...]
}}
"""
