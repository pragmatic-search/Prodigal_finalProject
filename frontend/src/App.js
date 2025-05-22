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
    const trimmedText = text.trim();

    if (!trimmedText) {
      setError('Please enter some text to summarize');
      return;
    }

    if (trimmedText.length < 100 || trimmedText.length > 5000) {
      setError('Text must be between 100-5000 characters');
      return;
    }

    setIsLoading(true);
    setError('');
    setSummary('');

    try {
      const response = await axios.post(
        'https://summarizer-backend.onrender.com/summarize',
        { text: trimmedText },
        {
          timeout: 30000,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.data && response.data.summary) {
        setSummary(response.data.summary);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to generate summary. Try a shorter text.'
      );
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
