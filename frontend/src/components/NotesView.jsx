/**
 * NotesView — Generate and display structured notes
 */
import { useState } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';
import '../styles/notes.css';

export default function NotesView({ documentId }) {
  const [topic, setTopic] = useState('');
  const [notes, setNotes] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateNotes = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setNotes(null);

    try {
      const result = await api.generateNotes(documentId, topic.trim(), topic.trim());
      setNotes(result);
    } catch (err) {
      alert('Error generating notes: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="notes-container animate-fadeIn">
      <div className="notes-header">
        <h2>📝 Smart Notes</h2>
        <p>Generate structured study notes on any topic from your document</p>
      </div>

      <div className="notes-input-row">
        <input
          className="input"
          type="text"
          placeholder="Enter a topic or question (e.g., 'Photosynthesis', 'What is machine learning?')"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && generateNotes()}
        />
        <button className="btn btn-primary" onClick={generateNotes} disabled={loading || !topic.trim()}>
          {loading ? 'Generating...' : 'Generate Notes'}
        </button>
      </div>

      {loading && <Loading text="Generating structured notes..." />}

      {notes && (
        <div className="notes-result card animate-fadeIn">
          <h3 className="notes-title">{notes.title}</h3>
          <div className="notes-content markdown-content" dangerouslySetInnerHTML={{ __html: formatMarkdown(notes.content) }} />

          {notes.key_points && notes.key_points.length > 0 && (
            <div className="notes-key-points">
              <h4>📌 Key Points</h4>
              <ul>
                {notes.key_points.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {!loading && !notes && (
        <div className="empty-state">
          <div className="empty-state-icon">📝</div>
          <h3>Enter a topic to generate notes</h3>
          <p>AI will create structured, easy-to-read study notes from your document.</p>
        </div>
      )}
    </div>
  );
}

function formatMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/### (.*)/g, '<h4>$1</h4>')
    .replace(/## (.*)/g, '<h3>$1</h3>')
    .replace(/# (.*)/g, '<h2>$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/- (.*)/g, '<li>$1</li>')
    .replace(/\n/g, '<br/>');
}
