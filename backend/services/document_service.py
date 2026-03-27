"""Document processing service — PDF parsing, chunking, and embedding."""

import os
import uuid
import fitz  # PyMuPDF
from fastapi import UploadFile
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from core.vectorstore import add_texts_to_collection
from models.document import Document


class DocumentService:
    """Handles document upload, parsing, chunking, and vector embedding."""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    async def save_upload(self, file: UploadFile) -> dict:
        """Save uploaded file to disk and return file metadata."""
        ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return {
            "filename": unique_name,
            "original_name": file.filename,
            "file_path": file_path,
            "file_type": ext.replace(".", ""),
            "file_size": len(content),
        }

    def parse_pdf(self, file_path: str) -> tuple[str, int]:
        """Extract text from a PDF file. Returns (text, num_pages)."""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n\n"
        num_pages = len(doc)
        doc.close()
        return text.strip(), num_pages

    def parse_text_file(self, file_path: str) -> str:
        """Read a plain text file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks, filtering out empty ones."""
        chunks = self.text_splitter.split_text(text)
        chunks = [c.strip() for c in chunks if c.strip()]
        return chunks

    def embed_and_store(self, chunks: list[str], collection_name: str) -> int:
        """Store chunks in ChromaDB (embeddings generated locally by ChromaDB)."""
        if not chunks:
            raise ValueError("No text chunks to embed. The document may be empty or unreadable.")

        # ChromaDB handles embedding locally — no batching needed for API limits
        add_texts_to_collection(collection_name, chunks)
        return len(chunks)

    async def process_document(self, file: UploadFile, db: Session) -> Document:
        """Full pipeline: save → parse → chunk → embed → store metadata."""
        # 1. Save file to disk
        file_meta = await self.save_upload(file)

        # 2. Create a unique collection name for this document
        collection_name = f"doc_{uuid.uuid4().hex[:12]}"

        # 3. Parse the document
        if file_meta["file_type"] == "pdf":
            text, num_pages = self.parse_pdf(file_meta["file_path"])
        elif file_meta["file_type"] in ("txt", "md", "text"):
            text = self.parse_text_file(file_meta["file_path"])
            num_pages = 1
        else:
            raise ValueError(f"Unsupported file type: {file_meta['file_type']}")

        # 4. Chunk the text
        chunks = self.chunk_text(text)

        # 5. Embed and store in vector DB
        num_chunks = self.embed_and_store(chunks, collection_name)

        # 6. Save document metadata to SQLite
        doc = Document(
            filename=file_meta["filename"],
            original_name=file_meta["original_name"],
            file_path=file_meta["file_path"],
            file_type=file_meta["file_type"],
            file_size=file_meta["file_size"],
            num_pages=num_pages,
            num_chunks=num_chunks,
            collection_name=collection_name,
            status="ready",
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return doc


# Singleton instance
document_service = DocumentService()
