/**
 * Sidebar — Navigation sidebar with feature tabs
 */
import '../styles/sidebar.css';

const features = [
  { id: 'chat', icon: '💬', label: 'Chat Q&A' },
  { id: 'notes', icon: '📝', label: 'Notes' },
  { id: 'mcq', icon: '❓', label: 'MCQs' },
  { id: 'summary', icon: '📋', label: 'Summary' },
  { id: 'flashcards', icon: '🃏', label: 'Flashcards' },
  { id: 'quiz', icon: '📊', label: 'Quiz Mode' },
];

export default function Sidebar({ activeTab, onTabChange, document: doc, onBack }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <button className="btn btn-ghost btn-sm" onClick={onBack}>← Back</button>
        <h2 className="gradient-text">StudyLM</h2>
      </div>

      {doc && (
        <div className="sidebar-doc">
          <span className="sidebar-doc-icon">📄</span>
          <div className="sidebar-doc-info">
            <p className="sidebar-doc-name" title={doc.original_name}>{doc.original_name}</p>
            <span className="sidebar-doc-meta">
              {doc.num_pages} pages · {doc.num_chunks} chunks
            </span>
          </div>
        </div>
      )}

      <nav className="sidebar-nav">
        {features.map((f) => (
          <button
            key={f.id}
            className={`sidebar-btn ${activeTab === f.id ? 'active' : ''}`}
            onClick={() => onTabChange(f.id)}
          >
            <span className="sidebar-btn-icon">{f.icon}</span>
            <span>{f.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <p>Powered by Gemini AI</p>
      </div>
    </aside>
  );
}
