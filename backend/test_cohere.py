from core.config import settings
from langchain_cohere import ChatCohere
import cohere

try:
    print("Testing RAW Cohere Embeddings...")
    client = cohere.Client(api_key=settings.COHERE_API_KEY)
    res = client.embed(texts=["Hello"], model=settings.EMBEDDING_MODEL, input_type="search_document")
    print("Embeddings OK! Length:", len(res.embeddings))
except Exception as e:
    print("Embeddings FAILED:", e)

for model_name in ["command-r", "command", "command-r-plus"]:
    try:
        print(f"\nTesting ChatCohere with {model_name}...")
        llm = ChatCohere(model=model_name, cohere_api_key=settings.COHERE_API_KEY, temperature=0.3)
        res = llm.invoke("Hi")
        print(f"SUCCESS with {model_name}: {res.content}")
        break  # If one works, we are good
    except Exception as e:
        print(f"FAILED with {model_name}:", e)
