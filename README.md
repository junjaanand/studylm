# 📚 StudyLM — AI-Powered Student Study Assistant

A NotebookLM-like application built for students. Upload your study material and let AI generate **smart notes**, **MCQs**, **summaries**, **flashcards**, and **interactive quizzes**.

## Tech Stack

- **Backend**: Python, FastAPI, LangChain, Google Gemini, ChromaDB
- **Frontend**: React (Vite), Vanilla CSS

## Getting Started

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

- 📄 Upload PDFs & text documents
- 📝 Generate structured notes from questions
- ❓ Auto-generate MCQs with explanations
- 💬 Chat with your documents (RAG-powered)
- 📋 Get topic/chapter summaries
- 🃏 Create flashcard decks
- 📊 Interactive quiz mode with scoring
