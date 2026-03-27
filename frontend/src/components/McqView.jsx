/**
 * McqView — Generate and display MCQs with interactive answer selection
 */
import { useState } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';
import '../styles/mcq.css';

export default function McqView({ documentId }) {
  const [topic, setTopic] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  const [mcqs, setMcqs] = useState(null);
  const [selected, setSelected] = useState({});
  const [revealed, setRevealed] = useState({});
  const [loading, setLoading] = useState(false);

  const generateMCQs = async () => {
    setLoading(true);
    setMcqs(null);
    setSelected({});
    setRevealed({});

    try {
      const result = await api.generateMCQs(documentId, topic.trim() || null, numQuestions);
      setMcqs(result);
    } catch (err) {
      alert('Error generating MCQs: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const selectOption = (qIndex, label) => {
    if (revealed[qIndex]) return;
    setSelected({ ...selected, [qIndex]: label });
  };

  const revealAnswer = (qIndex) => {
    setRevealed({ ...revealed, [qIndex]: true });
  };

  return (
    <div className="mcq-container animate-fadeIn">
      <div className="mcq-header">
        <h2>❓ MCQ Generator</h2>
        <p>Auto-generate practice questions from your study material</p>
      </div>

      <div className="mcq-controls">
        <input
          className="input"
          type="text"
          placeholder="Topic (optional — leave empty for general questions)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <select
          className="input mcq-select"
          value={numQuestions}
          onChange={(e) => setNumQuestions(parseInt(e.target.value))}
        >
          {[3, 5, 10, 15, 20].map((n) => (
            <option key={n} value={n}>{n} questions</option>
          ))}
        </select>
        <button className="btn btn-primary" onClick={generateMCQs} disabled={loading}>
          {loading ? 'Generating...' : 'Generate MCQs'}
        </button>
      </div>

      {loading && <Loading text="Generating MCQs..." />}

      {mcqs && mcqs.questions && (
        <div className="mcq-list">
          {mcqs.questions.map((q, qIdx) => (
            <div key={qIdx} className="mcq-card card animate-fadeIn" style={{ animationDelay: `${qIdx * 0.1}s` }}>
              <div className="mcq-q-header">
                <span className="mcq-q-num">Q{qIdx + 1}</span>
                <p className="mcq-question">{q.question}</p>
              </div>

              <div className="mcq-options">
                {q.options.map((opt) => {
                  const isSelected = selected[qIdx] === opt.label;
                  const isCorrect = revealed[qIdx] && opt.label === q.correct_answer;
                  const isWrong = revealed[qIdx] && isSelected && opt.label !== q.correct_answer;

                  return (
                    <button
                      key={opt.label}
                      className={`mcq-option ${isSelected ? 'selected' : ''} ${isCorrect ? 'correct' : ''} ${isWrong ? 'wrong' : ''}`}
                      onClick={() => selectOption(qIdx, opt.label)}
                    >
                      <span className="mcq-option-label">{opt.label}</span>
                      <span>{opt.text}</span>
                    </button>
                  );
                })}
              </div>

              {selected[qIdx] && !revealed[qIdx] && (
                <button className="btn btn-secondary btn-sm" onClick={() => revealAnswer(qIdx)}>
                  Check Answer
                </button>
              )}

              {revealed[qIdx] && (
                <div className={`mcq-explanation ${selected[qIdx] === q.correct_answer ? 'correct' : 'wrong'}`}>
                  <p>
                    <strong>{selected[qIdx] === q.correct_answer ? '✅ Correct!' : `❌ Wrong! Answer: ${q.correct_answer}`}</strong>
                  </p>
                  <p>{q.explanation}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {!loading && !mcqs && (
        <div className="empty-state">
          <div className="empty-state-icon">❓</div>
          <h3>Generate practice MCQs</h3>
          <p>Test your understanding with AI-generated multiple choice questions.</p>
        </div>
      )}
    </div>
  );
}
