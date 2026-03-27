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
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    async def save_upload(self, file: UploadFile) -> dict:
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
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n\n"
        num_pages = len(doc)
        doc.close()
        return text.strip(), num_pages

    def parse_text_file(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def chunk_text(self, text: str) -> list[str]:
        chunks = self.text_splitter.split_text(text)
        return [c.strip() for c in chunks if c.strip()]

    def embed_and_store(self, chunks: list[str], collection_name: str) -> int:
        if not chunks:
            raise ValueError("No text chunks found.")

        # Batch chunks to stay under Cohere's 96 chunk API limit per call
        batch_size = 90
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            add_texts_to_collection(collection_name, batch)
        return len(chunks)

    async def process_document(self, file: UploadFile, db: Session) -> Document:
        file_meta = await self.save_upload(file)
        collection_name = f"doc_{uuid.uuid4().hex[:12]}"

        if file_meta["file_type"] == "pdf":
            text, num_pages = self.parse_pdf(file_meta["file_path"])
        elif file_meta["file_type"] in ("txt", "md", "text"):
            text = self.parse_text_file(file_meta["file_path"])
            num_pages = 1
        else:
            raise ValueError(f"Unsupported file type: {file_meta['file_type']}")

        chunks = self.chunk_text(text)
        num_chunks = self.embed_and_store(chunks, collection_name)

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

document_service = DocumentService()
