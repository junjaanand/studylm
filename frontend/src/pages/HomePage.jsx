/**
 * HomePage — Landing page with document upload + document list
 */
import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import api from '../api/client.js';
import '../styles/home.css';

export default function HomePage({ onDocumentSelect }) {
  const [documents, setDocuments] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await api.getDocuments();
      setDocuments(docs);
    } catch {
      // Backend might not be running
    } finally {
      setLoadingDocs(false);
    }
  };

  const handleUploadComplete = (doc) => {
    setDocuments((prev) => [doc, ...prev]);
    onDocumentSelect(doc);
  };

  const handleDelete = async (e, docId) => {
    e.stopPropagation();
    if (!confirm('Delete this document?')) return;
    try {
      await api.deleteDocument(docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
    } catch (err) {
      alert('Error deleting: ' + err.message);
    }
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="home">
      {/* Hero Section */}
      <div className="home-hero">
        <h1 className="home-title">
          <span className="gradient-text">StudyLM</span>
        </h1>
        <p className="home-subtitle">
          Your AI-powered study assistant. Upload notes, generate MCQs, flashcards, summaries & more.
        </p>
        <FileUpload onUploadComplete={handleUploadComplete} />
      </div>

      {/* Previous Documents */}
      {documents.length > 0 && (
        <div className="home-docs animate-fadeIn">
          <h3>📚 Your Documents</h3>
          <div className="home-docs-grid">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="home-doc-card card"
                onClick={() => onDocumentSelect(doc)}
              >
                <div className="home-doc-icon">📄</div>
                <div className="home-doc-info">
                  <p className="home-doc-name">{doc.original_name}</p>
                  <span className="home-doc-meta">
                    {doc.num_pages} pages · {doc.num_chunks} chunks · {formatSize(doc.file_size)}
                  </span>
                </div>
                <div className="home-doc-actions">
                  <span className={`badge ${doc.status === 'ready' ? 'badge-success' : 'badge-info'}`}>
                    {doc.status}
                  </span>
                  <button className="btn btn-ghost btn-sm" onClick={(e) => handleDelete(e, doc.id)}>
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
