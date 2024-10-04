import './App.css';
import React, { useState, useEffect } from 'react';
import MgnScraperForm from './components/mgnScraperForm';
import useForm from './hooks/useForm';

function App() {
  const { data, setData, message, progress, downloadLink, error, handleSubmit } = useForm();
  
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>MGN Scraper</h1>
        <MgnScraperForm handleSubmit={handleSubmit} data={data} setData={setData} error={error} />

        {/* Dispaly Message and Progress */}
        {message && <p>{message}</p>}
        {progress > 0 && progress < 100 && (
          <div>
            <h3>Scraping Progress</h3>
            <progress value={progress} max="100">{progress}%</progress>
          </div>
        )}
        {downloadLink && (
          <div>
            <h3>Your Download is Ready:</h3>
            <a href={downloadLink} download="images.zip">
              <button>Download</button>
            </a>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
