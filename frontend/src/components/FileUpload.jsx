/**
 * FileUpload — Document upload component with drag-and-drop
 */
import { useState, useRef } from 'react';
import api from '../api/client.js';
import '../styles/upload.css';

export default function FileUpload({ onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState('');
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
  };

  const handleFile = async (file) => {
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'txt', 'md'].includes(ext)) {
      alert('Please upload a PDF, TXT, or MD file.');
      return;
    }

    setIsUploading(true);
    setUploadProgress('Uploading document...');

    try {
      setUploadProgress('Processing & embedding document...');
      const doc = await api.uploadDocument(file);
      setUploadProgress('Done!');
      if (onUploadComplete) onUploadComplete(doc);
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setIsUploading(false);
      setUploadProgress('');
    }
  };

  return (
    <div
      className={`upload-zone ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => !isUploading && fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.txt,.md"
        onChange={handleFileSelect}
        hidden
      />

      {isUploading ? (
        <div className="upload-progress">
          <div className="loading-spinner"></div>
          <p>{uploadProgress}</p>
        </div>
      ) : (
        <>
          <div className="upload-icon">📄</div>
          <h3>Drop your study material here</h3>
          <p>or click to browse</p>
          <span className="upload-formats">Supports PDF, TXT, MD</span>
        </>
      )}
    </div>
  );
}
