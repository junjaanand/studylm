"""Prompt template for summary generation."""

SUMMARY_PROMPT = """You are a study assistant. Based on the following study material, generate a concise yet comprehensive summary.

**Study Material:**
{context}

**Topic Focus:** {topic}

Generate a summary that includes:
1. A clear title
2. An overview paragraph
3. Main concepts explained concisely
4. Key takeaways

Format your response as JSON:
{{
    "title": "Summary title",
    "summary": "Full summary in markdown format",
    "key_concepts": ["concept 1", "concept 2", ...]
}}
"""
