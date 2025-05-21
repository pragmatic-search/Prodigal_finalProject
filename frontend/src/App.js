import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter some text to summarize');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://backend:8000/summarize', {
        text: text
      });
      setSummary(response.data.summary);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate summary');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>AI Text Summarizer</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to summarize (100-5000 characters)"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Summarizing...' : 'Summarize'}
        </button>
      </form>
      
      {error && <div className="error">{error}</div>}
      
      {isLoading && <div className="loading">Processing your text...</div>}
      
      {summary && (
        <div className="summary">
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;