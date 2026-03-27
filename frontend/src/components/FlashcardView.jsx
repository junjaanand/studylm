/**
 * FlashcardView — Interactive flashcard flip cards
 */
import { useState } from 'react';
import api from '../api/client.js';
import Loading from './Loading.jsx';
import '../styles/flashcard.css';

export default function FlashcardView({ documentId }) {
  const [topic, setTopic] = useState('');
  const [cards, setCards] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(false);

  const generateFlashcards = async () => {
    setLoading(true);
    setCards(null);
    setCurrentIndex(0);
    setFlipped(false);

    try {
      const result = await api.generateFlashcards(documentId, topic.trim() || null, 10);
      setCards(result);
    } catch (err) {
      alert('Error generating flashcards: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const nextCard = () => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex((prev) => (prev + 1) % cards.cards.length);
    }, 150);
  };

  const prevCard = () => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex((prev) => (prev - 1 + cards.cards.length) % cards.cards.length);
    }, 150);
  };

  return (
    <div className="flashcard-container animate-fadeIn">
      <div className="flashcard-header">
        <h2>🃏 Flashcards</h2>
        <p>Create flashcard decks for quick revision</p>
      </div>

      <div className="notes-input-row">
        <input
          className="input"
          type="text"
          placeholder="Topic (optional)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && generateFlashcards()}
        />
        <button className="btn btn-primary" onClick={generateFlashcards} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Flashcards'}
        </button>
      </div>

      {loading && <Loading text="Creating flashcards..." />}

      {cards && cards.cards && cards.cards.length > 0 && (
        <div className="flashcard-deck">
          <div className="flashcard-counter">
            Card {currentIndex + 1} of {cards.cards.length}
          </div>

          <div className={`flashcard ${flipped ? 'flipped' : ''}`} onClick={() => setFlipped(!flipped)}>
            <div className="flashcard-inner">
              <div className="flashcard-front">
                <span className="flashcard-label">Question</span>
                <p>{cards.cards[currentIndex].front}</p>
                <span className="flashcard-hint">Click to flip</span>
              </div>
              <div className="flashcard-back">
                <span className="flashcard-label">Answer</span>
                <p>{cards.cards[currentIndex].back}</p>
                <span className="flashcard-hint">Click to flip back</span>
              </div>
            </div>
          </div>

          <div className="flashcard-nav">
            <button className="btn btn-secondary" onClick={prevCard}>← Previous</button>
            <button className="btn btn-secondary" onClick={nextCard}>Next →</button>
          </div>
        </div>
      )}

      {!loading && !cards && (
        <div className="empty-state">
          <div className="empty-state-icon">🃏</div>
          <h3>Generate flashcards</h3>
          <p>Quick front-and-back cards for effective revision.</p>
        </div>
      )}
    </div>
  );
}
