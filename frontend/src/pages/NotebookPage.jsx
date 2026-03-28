/**
 * NotebookPage — Main workspace after uploading a document
 */
import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import NotesView from '../components/NotesView';
import McqView from '../components/McqView';
import SummaryView from '../components/SummaryView';
import FlashcardView from '../components/FlashcardView';
import QuizView from '../components/QuizView';
import MindmapView from '../components/MindmapView';
import '../styles/notebook.css';

const tabComponents = {
  chat: ChatWindow,
  notes: NotesView,
  mcq: McqView,
  summary: SummaryView,
  flashcards: FlashcardView,
  quiz: QuizView,
  mindmap: MindmapView,
};

export default function NotebookPage({ document: doc, onBack }) {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div className="notebook">
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        document={doc}
        onBack={onBack}
      />
      <main className="notebook-main">
        {Object.entries(tabComponents).map(([key, Component]) => (
          <div 
            key={key} 
            style={{ 
              display: activeTab === key ? 'block' : 'none', 
              height: '100%', 
              width: '100%' 
            }}
          >
            <Component documentId={doc.id} />
          </div>
        ))}
      </main>
    </div>
  );
}
