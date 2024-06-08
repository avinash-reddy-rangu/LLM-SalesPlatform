import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("Home");
  const [role, setRole] = useState("");
  const [tone, setTone] = useState("");
  const [instructions, setInstructions] = useState("");
  const [purpose, setPurpose] = useState("");
  const [prompt, setPrompt] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [message, setMessage] = useState("");
  const [documents, setDocuments] = useState([]);
  const [savedPrompts, setSavedPrompts] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState("");

  useEffect(() => {
    setSavedPrompts([]);
  }, []);

  useEffect(() => {
    if (selectedPrompt) {
      const savedPrompt = savedPrompts.find((p) => p === selectedPrompt);
      if (savedPrompt) {
        const [
          roleValue,
          toneValue,
          instructionsValue,
          purposeValue,
          promptValue,
        ] = savedPrompt.split(",");
        setRole(roleValue);
        setTone(toneValue);
        setInstructions(instructionsValue);
        setPurpose(purposeValue);
        setPrompt(promptValue);
      }
    }
  }, [selectedPrompt, savedPrompts]);

  const handleSubmit = (e) => {
    e.preventDefault();
    // ikkada api call cheyali
//     const randomName = Prompt-${Math.floor(Math.random() * 1000)};
    const randomName = "Prompt-1"
    setSavedPrompts([...savedPrompts, { name: randomName, prompt }]);
    setPrompt("");
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      setChatHistory([...chatHistory, { text: message }]);
      setMessage("");
    }
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    // ikkada api call
    setTimeout(() => {
      const uploadedFiles = files.map((file) => ({
        name: file.name,
        type: "pdf",
      }));
      setDocuments([...documents, ...uploadedFiles]);
    }, 1000);
  };

  const handlePromptSelect = (selectedPrompt) => {
    const selected = savedPrompts.find(
      (prompt) => prompt.name === selectedPrompt
    );
    if (selected) {
      const [
        roleValue,
        toneValue,
        instructionsValue,
        purposeValue,
        promptValue,
      ] = selected.prompt.split(",");
      setRole(roleValue);
      setTone(toneValue);
      setInstructions(instructionsValue);
      setPurpose(purposeValue);
      setPrompt(promptValue);
      setSelectedPrompt(selectedPrompt);
    }
  };

  return (
    <div className="App">
      <header>
        <img
          src="/jpm-logo.png"
          alt="J.P. Morgan Chase Logo"
          className="logo"
        />
        <h1>
          AI-Powered Client Interaction and Sales Support Platform using Large
          Language Models
        </h1>
      </header>
      <div className="content">
        <nav className="sidebar">
          <ul>
            <li
              className={activeTab === "Home" ? "active" : ""}
              onClick={() => setActiveTab("Home")}
            >
              Home
            </li>
            <li
              className={activeTab === "AI Assistant" ? "active" : ""}
              onClick={() => setActiveTab("AI Assistant")}
            >
              AI Assistant
            </li>
            <li
              className={activeTab === "Content Library" ? "active" : ""}
              onClick={() => setActiveTab("Content Library")}
            >
              Content Library
            </li>
            <li
              className={activeTab === "Prompt Library" ? "active" : ""}
              onClick={() => setActiveTab("Prompt Library")}
            >
              Prompt Library
            </li>
          </ul>
        </nav>
        <main className="main-content">
          {activeTab === "Home" && (
            <div className="home">
              <h2>Login Details</h2>
              <p>Banker Name: John Doe</p>
              <p>Position: Senior Banker</p>
            </div>
          )}
          {activeTab === "AI Assistant" && (
            <div className="ai-assistant-container">
              <div className="chat-interface">
                <h2>AI Assistant</h2>
                <div className="chat-window">
                  {chatHistory.map((chat, index) => (
                    <div key={index} className="chat-message">
                      {chat.text ? (
                        <p>{chat.text}</p>
                      ) : (
                        <>
                          <p>
                            <strong>Role:</strong> {chat.role}
                          </p>
                          <p>
                            <strong>Tone:</strong> {chat.tone}
                          </p>
                          <p>
                            <strong>Instructions:</strong> {chat.instructions}
                          </p>
                          <p>
                            <strong>Purpose:</strong> {chat.purpose}
                          </p>
                          <p>
                            <strong>Prompt:</strong> {chat.prompt}
                          </p>
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
                  <button onClick={handleSendMessage}>{">"}</button>
                </div>
              </div>
              <div className="prompt-options">
                <h2>Prompt Options</h2>
                <div>
                  <label>Select Prompt</label>
                  <select
                    value={selectedPrompt}
                    onChange={(e) => handlePromptSelect(e.target.value)}
                  >
                    <option value="">Select a Prompt</option>
                    {savedPrompts.map((prompt) => (
                      <option key={prompt.name} value={prompt.name}>
                        {prompt.name}
                      </option>
                    ))}
                  </select>
                </div>
                <form onSubmit={handleSubmit}>
                  <div>
                    <label>Role</label>
                    <input
                      type="text"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Tone</label>
                    <input
                      type="text"
                      value={tone}
                      onChange={(e) => setTone(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Instructions</label>
                    <input
                      type="text"
                      value={instructions}
                      onChange={(e) => setInstructions(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Purpose</label>
                    <input
                      type="text"
                      value={purpose}
                      onChange={(e) => setPurpose(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Prompt</label>
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                    />
                  </div>
                  <button type="submit" className="submit-button">
                    Submit
                  </button>
                </form>
              </div>
            </div>
          )}
          {activeTab === "Content Library" && (
            <div className="content-library">
              <h2>Content Library</h2>
              <input type="file" multiple onChange={handleFileUpload} />
              <div className="uploaded-files">
                <h2>Uploaded files</h2>
                {documents.map((doc, index) => (
                  <div key={index} className="file-item">
                    <span className="file-icon">{doc.type.toUpperCase()}</span>
                    <span className="file-name">{doc.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {activeTab === "Prompt Library" && (
            <div className="prompt-options">
              <div className="prompt-form">
                <h2>Prompt Options</h2>
                <form onSubmit={handleSubmit}>
                  <div>
                    <label>Role</label>
                    <input
                      type="text"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Tone</label>
                    <input
                      type="text"
                      value={tone}
                      onChange={(e) => setTone(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Instructions</label>
                    <input
                      type="text"
                      value={instructions}
                      onChange={(e) => setInstructions(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Purpose</label>
                    <input
                      type="text"
                      value={purpose}
                      onChange={(e) => setPurpose(e.target.value)}
                    />
                  </div>
                  <div>
                    <label>Prompt</label>
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                    />
                  </div>
                  <button type="submit" className="submit-button">
                    Submit
                  </button>
                </form>
              </div>
              <div className="saved-prompts">
                <h3>Saved Prompts</h3>
                <ul>
                  {savedPrompts.map((item, index) => (
                    <li key={index}>{item.name}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;