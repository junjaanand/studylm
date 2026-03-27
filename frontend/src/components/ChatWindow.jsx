/**
 * ChatWindow — Q&A chat interface for document-grounded conversations
 */
import { useState, useRef, useEffect } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';
import '../styles/chat.css';

export default function ChatWindow({ documentId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setLoading(true);

    try {
      const result = await api.chatAsk(documentId, question);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: result.answer, sources: result.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.', error: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state animate-fadeIn">
            <div className="empty-state-icon">💬</div>
            <h3>Ask anything about your document</h3>
            <p>Your answers are grounded in the uploaded study material.</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`chat-msg ${msg.role} ${msg.error ? 'error' : ''} animate-fadeIn`}>
            <div className="chat-msg-avatar">
              {msg.role === 'user' ? '🧑‍🎓' : '🤖'}
            </div>
            <div className="chat-msg-content">
              <div className="chat-msg-text markdown-content" dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }} />
              {msg.sources && msg.sources.length > 0 && (
                <div className="chat-sources">
                  <span className="chat-sources-label">📚 Sources:</span>
                  {msg.sources.map((s, j) => (
                    <span key={j} className="chat-source-chip">{s.substring(0, 80)}...</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && <Loading text="Thinking..." />}
        <div ref={endRef} />
      </div>

      <div className="chat-input-bar">
        <textarea
          className="chat-input input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your study material..."
          rows={1}
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={sendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

function formatMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br/>');
}
