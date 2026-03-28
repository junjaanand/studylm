from langchain_core.prompts import PromptTemplate

MINDMAP_PROMPT = """You are an expert educational AI that creates visual mind maps and flowcharts.

Your task is to read the provided text chunks and generate a valid Mermaid.js flowchart code (`graph TD`) that maps out the core concepts, relationships, and hierarchies of the document.

RULES:
1. ONLY output valid Mermaid.js code. Do not wrap the code in markdown blocks (no ```mermaid ... ```).
2. Start the code exactly with `graph TD`.
3. Keep node labels short and concise (e.g. `A[Core Concept]`).
4. Avoid using special characters, quotes, or parentheses inside node definitions, as they can break the Mermaid renderer.
5. Create a logical hierarchy: Main Topic at the top, branching down into sub-topics and details.
6. Connect at least 15-20 nodes to give a comprehensive visual overview.

Example Output format exactly:
graph TD
    A[Machine Learning] --> B[Supervised]
    A --> C[Unsupervised]
    B --> D[Classification]
    B --> E[Regression]
    C --> F[Clustering]

CONTEXT:
{context}

Generate the Mermaid flowchart code now (and absolutely nothing else):
"""

mindmap_prompt_template = PromptTemplate(
    template=MINDMAP_PROMPT,
    input_variables=["context"]
)
