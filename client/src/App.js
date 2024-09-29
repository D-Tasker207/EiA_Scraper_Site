import './App.css';
import React, { useState, useEffect } from 'react';
import MgnScraperForm from './components/mgnScraperForm';
import useForm from './hooks/useForm';

function App() {
  const { data, setData, error, handleSubmit } = useForm();
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {i
    const socket = new WebSocket('ws://localhost:3001');

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);

      if(response.type === 'progress') {
        setProgress(response.data);
      } else if(response.type === 'message') {
        setMessage(response.data);
      }
    };

    return () => {
      socket.close();
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>MGN Scraper</h1>
        <MgnScraperForm handleSubmit={handleSubmit} data={data} setData={setData} error={error} />

        {/* Dispaly Message and Progress */}
        {serverMessage && <p>{message}</p>}
        {progress > 0 && progress < 100 && (
          <div>
            <h3>Scraping Progress</h3>
            <progress value={progress} max="100">{progress}%</progress>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
