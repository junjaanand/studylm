import { useState, useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import api from '../api/client';
import '../styles/notes.css'; // Reusing general view styles

export default function MindmapView({ documentId }) {
  const [mindmapCode, setMindmapCode] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [topic, setTopic] = useState('');
  const renderRef = useRef(null);

  // Initialize mermaid exactly once
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: 'dark' });
  }, []);

  const handleGenerate = async () => {
    if (!documentId) return;
    setIsLoading(true);
    setError(null);
    setMindmapCode(null);

    try {
      const res = await api.generateMindmap(documentId, topic);
      setMindmapCode(res.mermaid_code);
    } catch (err) {
      setError(err.message || 'Failed to generate mind map.');
    } finally {
      setIsLoading(false);
    }
  };

  // Render the SVG instantly when fresh mermaid code arrives
  useEffect(() => {
    if (mindmapCode && renderRef.current) {
      const renderDiagram = async () => {
        try {
          renderRef.current.innerHTML = '';
          const { svg } = await mermaid.render('mermaid-chart', mindmapCode);
          renderRef.current.innerHTML = svg;
        } catch (err) {
          setError('Failed to render the diagram. The AI output might have been too complex.');
        }
      };
      renderDiagram();
    }
  }, [mindmapCode]);

  return (
    <div className="view-container">
      <div className="view-header">
        <h2>AI Mind Map & Flowchart</h2>
        <div className="settings-row">
          <input 
            type="text" 
            placeholder="Focus area (optional)" 
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <button onClick={handleGenerate} disabled={isLoading || !documentId}>
            {isLoading ? 'Mapping...' : 'Generate Map'}
          </button>
        </div>
      </div>
      
      {error && <div className="error-box">{error}</div>}

      <div className="mindmap-content" style={{ padding: '20px', background: '#111', borderRadius: '12px', marginTop: '20px', overflow: 'auto', minHeight: '400px' }}>
        {!mindmapCode && !isLoading && !error && (
            <p className="placeholder-text">Click generate to visualize the document relationships.</p>
        )}
        {isLoading && (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Analyzing document structure...</p>
            </div>
        )}
        <div ref={renderRef} className="mermaid-diagram" style={{ display: 'flex', justifyContent: 'center' }}></div>
      </div>
      
      {mindmapCode && (
          <details style={{ marginTop: '20px', cursor: 'pointer', color: '#888' }}>
            <summary>View raw Mermaid code</summary>
            <pre style={{ padding: '10px', background: '#000', borderRadius: '4px', overflowX: 'auto', fontSize: '12px' }}>
                {mindmapCode}
            </pre>
          </details>
      )}
    </div>
  );
}
