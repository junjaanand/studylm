/**
 * StudyLM — Main App Component
 * Handles page routing between Home and Notebook views
 */
import { useState } from 'react';
import HomePage from './pages/HomePage';
import NotebookPage from './pages/NotebookPage';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedDoc, setSelectedDoc] = useState(null);

  const handleDocumentSelect = (doc) => {
    setSelectedDoc(doc);
    setCurrentPage('notebook');
  };

  const handleBack = () => {
    setCurrentPage('home');
    setSelectedDoc(null);
  };

  return (
    <>
      {currentPage === 'home' && (
        <HomePage onDocumentSelect={handleDocumentSelect} />
      )}
      {currentPage === 'notebook' && selectedDoc && (
        <NotebookPage document={selectedDoc} onBack={handleBack} />
      )}
    </>
  );
}

export default App;
