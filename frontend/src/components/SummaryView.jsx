/**
 * SummaryView — Generate and display document summaries
 */
import { useState } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';

export default function SummaryView({ documentId }) {
  const [topic, setTopic] = useState('');
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateSummary = async () => {
    setLoading(true);
    setSummary(null);

    try {
      const result = await api.generateSummary(documentId, topic.trim() || null);
      setSummary(result);
    } catch (err) {
      alert('Error generating summary: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="notes-container animate-fadeIn">
      <div className="notes-header">
        <h2>📋 Summary</h2>
        <p>Get a concise summary of your document or a specific topic</p>
      </div>

      <div className="notes-input-row">
        <input
          className="input"
          type="text"
          placeholder="Topic (optional — leave empty for full document summary)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && generateSummary()}
        />
        <button className="btn btn-primary" onClick={generateSummary} disabled={loading}>
          {loading ? 'Summarizing...' : 'Generate Summary'}
        </button>
      </div>

      {loading && <Loading text="Generating summary..." />}

      {summary && (
        <div className="notes-result card animate-fadeIn">
          <h3 className="notes-title">{summary.title}</h3>
          <div className="notes-content markdown-content" dangerouslySetInnerHTML={{ __html: formatMarkdown(summary.summary) }} />

          {summary.key_concepts && summary.key_concepts.length > 0 && (
            <div className="notes-key-points">
              <h4>🔑 Key Concepts</h4>
              <ul>
                {summary.key_concepts.map((concept, i) => (
                  <li key={i}>{concept}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {!loading && !summary && (
        <div className="empty-state">
          <div className="empty-state-icon">📋</div>
          <h3>Generate a summary</h3>
          <p>Get a condensed overview of your study material.</p>
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
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/- (.*)/g, '<li>$1</li>')
    .replace(/\n/g, '<br/>');
}
