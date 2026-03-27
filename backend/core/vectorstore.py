"""ChromaDB vector store manager — uses Cohere API for embeddings to save RAM."""

import chromadb
import cohere
from core.config import settings

def get_chroma_client():
    """Get a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=settings.CHROMA_PATH)

def add_texts_to_collection(collection_name: str, texts: list[str], metadatas: list[dict] = None):
    """Add texts with their embeddings to a ChromaDB collection."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    # Use Cohere API to drastically lower server RAM usage
    co = cohere.Client(api_key=settings.COHERE_API_KEY)
    response = co.embed(texts=texts, model=settings.EMBEDDING_MODEL, input_type="search_document")
    embeddings = response.embeddings

    ids = [f"{collection_name}_{i}" for i in range(collection.count(), collection.count() + len(texts))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas or [{"chunk_index": i} for i in range(len(texts))],
        ids=ids,
    )

def query_collection(collection_name: str, query: str, k: int = 5) -> list[str]:
    """Query a collection and return the top-k most relevant text chunks."""
    client = get_chroma_client()

    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        return []
    
    if collection.count() == 0:
        return []

    co = cohere.Client(api_key=settings.COHERE_API_KEY)
    response = co.embed(texts=[query], model=settings.EMBEDDING_MODEL, input_type="search_query")
    query_emb = response.embeddings[0]

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=min(k, collection.count()),
    )

    if results and results["documents"]:
        return results["documents"][0]
    return []

def delete_collection(collection_name: str):
    """Delete a collection from ChromaDB."""
    client = get_chroma_client()
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
