"""LLM setup using Groq for text generation."""

from langchain_groq import ChatGroq
from core.config import settings
import re


def clean_json_response(text: str) -> str:
    """Extract JSON robustly by finding the outermost brackets."""
    text = text.strip()
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    # Find the outermost { or [
    start_idx = -1
    for i, char in enumerate(text):
        if char in ('{', '['):
            start_idx = i
            break

    end_idx = -1
    for i in range(len(text) - 1, -1, -1):
        if text[i] in ('}', ']'):
            end_idx = i
            break

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return text[start_idx:end_idx+1]

    return text


def get_llm():
    """Get the configured LLM instance (Groq for fast text generation)."""
    return ChatGroq(
        model=settings.LLM_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.3,
    )
