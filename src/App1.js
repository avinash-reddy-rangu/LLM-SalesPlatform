import React, { useState } from 'react';
import './App1.css';

function App() {
  const [role, setRole] = useState('');
  const [tone, setTone] = useState('');
  const [instructions, setInstructions] = useState('');
  const [purpose, setPurpose] = useState('');
  const [prompt, setPrompt] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const newChat = { role, tone, instructions, purpose, prompt };
    setChatHistory([...chatHistory, newChat]);
    setPrompt('');
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      setChatHistory([...chatHistory, { text: message }]);
      setMessage('');
    }
  };

  return (
    <div className="App">
      <header>
        <img src="/jpm-logo.png" alt="J.P. Morgan Chase Logo" className="logo" />
        <h1>AI-Powered Client Interaction and Sales Support Platform using Large Language Models</h1>
      </header>
      <div className="content">
        <div className="chat-interface">
          <h2>AI Assistant</h2>
          <div className="chat-window">
            {chatHistory.map((chat, index) => (
              <div key={index} className="chat-message">
                {chat.text ? <p>{chat.text}</p> : (
                  <>
                    <p><strong>Role:</strong> {chat.role}</p>
                    <p><strong>Tone:</strong> {chat.tone}</p>
                    <p><strong>Instructions:</strong> {chat.instructions}</p>
                    <p><strong>Purpose:</strong> {chat.purpose}</p>
                    <p><strong>Prompt:</strong> {chat.prompt}</p>
                  </>
                )}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
            />
            <button onClick={handleSendMessage}>{'>'}</button>
          </div>
        </div>
        <div className="prompt-options">
          <h2>Prompt Options</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <label>Role</label>
              <input type="text" value={role} onChange={(e) => setRole(e.target.value)} />
            </div>
            <div>
              <label>Tone</label>
              <input type="text" value={tone} onChange={(e) => setTone(e.target.value)} />
            </div>
            <div>
              <label>Instructions</label>
              <input type="text" value={instructions} onChange={(e) => setInstructions(e.target.value)} />
            </div>
            <div>
              <label>Purpose</label>
              <input type="text" value={purpose} onChange={(e) => setPurpose(e.target.value)} />
            </div>
            <div>
              <label>Prompt</label>
              <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            </div>
            <button type="submit" className="submit-button">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
