import React, { useState } from "react";
import "./Chat.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    const currentInput = input;
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: currentInput }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch response");
      }

      const data = await response.json();
      
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer || "Sorry, I couldn't process that request.",
        },
      ]);
    } catch (error) {
      console.error("Error asking question:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, there was an error connecting to the server.",
        },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>
          RAG <span className="gradient-text">Assistant</span>
        </h1>
        <p>Ask anything and get answers from your documents</p>
      </header>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">✨</div>
            <h2>How can I help you today?</h2>
            <p>
              Type your question below to start exploring your knowledge base.
            </p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`chat-bubble-wrapper ${msg.role}`}>
              <div className="chat-avatar">
                {msg.role === "user" ? "U" : "AI"}
              </div>
              <div className="chat-bubble">{msg.content}</div>
            </div>
          ))
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="chat-input"
        />
        <button
          type="submit"
          className="chat-submit-btn"
          disabled={!input.trim()}
        >
          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            stroke="currentColor"
            strokeWidth="2"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </form>
    </div>
  );
};

export default Chat;
