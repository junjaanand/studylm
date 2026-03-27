/**
 * QuizView — Interactive timed quiz mode
 */
import { useState, useEffect } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';
import '../styles/quiz.css';

export default function QuizView({ documentId }) {
  const [topic, setTopic] = useState('');
  const [numQuestions, setNumQuestions] = useState(10);
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    let interval;
    if (quiz && !results) {
      interval = setInterval(() => setTimer((t) => t + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [quiz, results]);

  const startQuiz = async () => {
    setLoading(true);
    setQuiz(null);
    setResults(null);
    setAnswers([]);
    setTimer(0);

    try {
      const result = await api.startQuiz(documentId, topic.trim() || null, numQuestions);
      setQuiz(result);
      setAnswers(new Array(result.questions.length).fill(''));
    } catch (err) {
      alert('Error starting quiz: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qIndex, label) => {
    if (results) return;
    const newAnswers = [...answers];
    newAnswers[qIndex] = label;
    setAnswers(newAnswers);
  };

  const submitQuiz = async () => {
    setSubmitting(true);
    try {
      const result = await api.submitQuiz(quiz.quiz_id, answers);
      setResults(result);
    } catch (err) {
      alert('Error submitting quiz: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const answeredCount = answers.filter((a) => a !== '').length;

  return (
    <div className="quiz-container animate-fadeIn">
      {/* Setup screen */}
      {!quiz && !results && (
        <>
          <div className="quiz-setup">
            <h2>📊 Quiz Mode</h2>
            <p>Test your knowledge with a timed interactive quiz</p>

            <div className="quiz-setup-form">
              <input
                className="input"
                type="text"
                placeholder="Topic (optional)"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
              <select
                className="input mcq-select"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              >
                {[5, 10, 15, 20].map((n) => (
                  <option key={n} value={n}>{n} questions</option>
                ))}
              </select>
              <button className="btn btn-primary btn-lg" onClick={startQuiz} disabled={loading}>
                {loading ? 'Preparing Quiz...' : '🚀 Start Quiz'}
              </button>
            </div>
          </div>
          {loading && <Loading text="Generating quiz questions..." />}
        </>
      )}

      {/* Quiz in progress */}
      {quiz && !results && (
        <>
          <div className="quiz-toolbar">
            <div className="quiz-timer">⏱ {formatTime(timer)}</div>
            <div className="quiz-progress">{answeredCount} / {quiz.questions.length} answered</div>
            <button
              className="btn btn-primary"
              onClick={submitQuiz}
              disabled={submitting || answeredCount === 0}
            >
              {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
          </div>

          <div className="quiz-questions">
            {quiz.questions.map((q, qIdx) => (
              <div key={qIdx} className="mcq-card card animate-fadeIn">
                <div className="mcq-q-header">
                  <span className="mcq-q-num">Q{qIdx + 1}</span>
                  <p className="mcq-question">{q.question}</p>
                </div>
                <div className="mcq-options">
                  {q.options.map((opt) => (
                    <button
                      key={opt.label}
                      className={`mcq-option ${answers[qIdx] === opt.label ? 'selected' : ''}`}
                      onClick={() => selectAnswer(qIdx, opt.label)}
                    >
                      <span className="mcq-option-label">{opt.label}</span>
                      <span>{opt.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Results */}
      {results && (
        <div className="quiz-results animate-fadeIn">
          <div className="quiz-score-card">
            <h2>Quiz Complete!</h2>
            <div className="quiz-score-circle">
              <span className="quiz-score-value">{results.score_percentage}%</span>
            </div>
            <p className="quiz-score-detail">
              {results.correct_answers} correct out of {results.total_questions} questions
            </p>
            <p className="quiz-score-time">Time: {formatTime(timer)}</p>
          </div>

          <div className="quiz-results-list">
            {results.results.map((r, i) => (
              <div key={i} className={`mcq-card card ${r.is_correct ? 'quiz-correct' : 'quiz-wrong'}`}>
                <div className="mcq-q-header">
                  <span className="mcq-q-num">{r.is_correct ? '✅' : '❌'}</span>
                  <p className="mcq-question">{r.question}</p>
                </div>
                <p className="quiz-result-answer">
                  Your answer: <strong>{r.your_answer || '(skipped)'}</strong>
                  {!r.is_correct && <> · Correct: <strong className="quiz-correct-label">{r.correct_answer}</strong></>}
                </p>
                {r.explanation && (
                  <div className={`mcq-explanation ${r.is_correct ? 'correct' : 'wrong'}`}>
                    <p>{r.explanation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          <button className="btn btn-primary btn-lg" onClick={() => { setQuiz(null); setResults(null); }}>
            🔄 Take Another Quiz
          </button>
        </div>
      )}
    </div>
  );
}
