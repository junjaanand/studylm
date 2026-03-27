"""ChromaDB vector store manager — uses ChromaDB's built-in local embeddings (no API calls)."""

import chromadb
from core.config import settings


def get_chroma_client():
    """Get a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=settings.CHROMA_PATH)


def add_texts_to_collection(collection_name: str, texts: list[str], metadatas: list[dict] = None):
    """Add texts to a ChromaDB collection. ChromaDB auto-generates embeddings locally."""
    client = get_chroma_client()
    # ChromaDB uses its built-in default embedding function (all-MiniLM-L6-v2)
    # No external API calls needed — runs instantly on local CPU
    collection = client.get_or_create_collection(name=collection_name)

    # Create IDs for each document
    ids = [f"{collection_name}_{i}" for i in range(collection.count(), collection.count() + len(texts))]

    collection.add(
        documents=texts,
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

    results = collection.query(
        query_texts=[query],
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
