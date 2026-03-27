/**
 * Axios-like API client for communicating with the StudyLM backend.
 * Uses native fetch for zero dependencies.
 */

// Import Vercel environment URL or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Remove Content-Type for FormData (file uploads)
  if (options.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

const api = {
  // --- Documents ---
  uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/documents/upload', { method: 'POST', body: formData });
  },

  getDocuments() {
    return request('/documents/');
  },

  getDocument(documentId) {
    return request(`/documents/${documentId}`);
  },

  deleteDocument(documentId) {
    return request(`/documents/${documentId}`, { method: 'DELETE' });
  },

  // --- Notes ---
  generateNotes(documentId, topic = null, question = null) {
    return request('/notes/generate', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, topic, question }),
    });
  },

  // --- MCQ ---
  generateMCQs(documentId, topic = null, numQuestions = 5) {
    return request('/mcq/generate', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, topic, num_questions: numQuestions }),
    });
  },

  // --- Chat ---
  chatAsk(documentId, question) {
    return request('/chat/ask', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, question }),
    });
  },

  // --- Summary ---
  generateSummary(documentId, topic = null) {
    return request('/summary/generate', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, topic }),
    });
  },

  // --- Flashcards ---
  generateFlashcards(documentId, topic = null, numCards = 10) {
    return request('/flashcards/generate', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, topic, num_cards: numCards }),
    });
  },

  // --- Quiz ---
  startQuiz(documentId, topic = null, numQuestions = 10) {
    return request('/quiz/start', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId, topic, num_questions: numQuestions }),
    });
  },

  submitQuiz(quizId, answers) {
    return request('/quiz/submit', {
      method: 'POST',
      body: JSON.stringify({ quiz_id: quizId, answers }),
    });
  },
};

export default api;
