import React, { useState } from "react";
import ClipLoader from "react-spinners/ClipLoader";
import "../styles/Chat.css";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const startTime = Date.now();
    setLoading(true);
    const MIN_SPINNER_TIME = 500; // milliseconds

    try {
      const response = await fetch("http://localhost:8000/api/bra-fitting", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input })
      });

      if (!response.ok) {
        let errorMsg = "An error occurred. Please try again.";
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || errorMsg;
        } catch {}
        throw new Error(errorMsg);
      }

      const data = await response.json();

      setMessages([...messages, {
        text: input,
        isUser: true
      }, {
        text: `Recommended Size: ${data.recommendation}`,
        reasoning: data.reasoning,
        fitTips: data.fit_tips,
        issues: data.identified_issues,
        confidence: data.confidence,
        sister_sizes: data.sister_sizes,
        isUser: false
      }]);
      
      setInput("");
    } catch (error) {
      console.error(error);
      setError(error.message || "Network error. Please try again.");
    } finally {
      const elapsedTime = Date.now() - startTime;
      if (elapsedTime < MIN_SPINNER_TIME) {
        setTimeout(() => {
          setLoading(false);
        }, MIN_SPINNER_TIME - elapsedTime);
      } else {
        setLoading(false);
      }
    }
  };

  const handleClear = () => {
    setMessages([]);
    setInput("");
    setError(null);
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {loading && (
          <div className="loading-indicator">
            <ClipLoader color="#000000" size={15} />
            <span style={{ marginLeft: "1em" }}>Loading...</span>
          </div>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.isUser ? "user" : "bot"}`}>
            {msg.isUser ? (
              msg.text
            ) : (
              <div className="recommendation-card">
                <div><strong>Recommended Size:</strong> {msg.text.replace('Recommended Size: ', '')}</div>
                {msg.confidence !== undefined && (
                  <div><strong>Confidence:</strong> {Math.round(msg.confidence * 100)}%</div>
                )}
                {msg.reasoning && (
                  <div><strong>Reasoning:</strong> {msg.reasoning}</div>
                )}
                {msg.fitTips && (
                  <div><strong>Fit Tips:</strong> {msg.fitTips}</div>
                )}
                {msg.issues && msg.issues.length > 0 && (
                  <div><strong>Identified Issues:</strong> {msg.issues.join(', ')}</div>
                )}
                {msg.sister_sizes && msg.sister_sizes.length > 0 && (
                  <div><strong>Sister Sizes:</strong> {msg.sister_sizes.join(', ')}</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      {error && (
        <div className="error-message" style={{ color: 'red', margin: '1em 0' }}>
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            if (error) setError(null);
          }}
          placeholder="Enter your measurements and fit issues..."
        />
        <button type="submit">Get Recommendation</button>
        <button
          type="button"
          onClick={handleClear}
          style={{ marginLeft: "1em", background: "#eee", color: "#333" }}
        >
          Clear
        </button>
      </form>
      <div className="input-guidance">
        <small>
          <strong>Tip:</strong> Enter your underbust and bust measurements (e.g., <em>34 underbust, 38 bust</em>) and describe any fit issues (e.g., <em>band rides up, straps keep falling off</em>).
        </small>
      </div>
    </div>
  );
};

export default ChatInterface;
