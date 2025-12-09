import React, { useState } from "react";
import api from "../api/apiClient";
import "../styles/components.css";

export default function ChatPanel({ filters = {} }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [webFetch, setWebFetch] = useState(false);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { from: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    try {
      const res = await api.post("/chat", {
        session_id: "demo",
        message: input,
        web_fetch: webFetch,
        filters,
      });

      const assistant = {
        from: "assistant",
        text: res.data.answer,
        citations: res.data.citations || [],
      };

      setMessages((m) => [...m, assistant]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { from: "assistant", text: "Error: " + err.message },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="chat-panel-container">
      <h3>Chat</h3>

      <label style={{ fontSize: 12 }}>
        <input
          type="checkbox"
          checked={webFetch}
          onChange={(e) => setWebFetch(e.target.checked)}
        />
        Allow web lookup
      </label>

      <div className="chat-messages-container">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${
              msg.from === "user" ? "user" : "assistant"
            }`}
          >
            <div className="chat-bubble">
              {msg.text}

              {msg.citations && msg.citations.length > 0 && (
                <div className="citations">
                  <strong>Sources:</strong>
                  <ul>
                    {msg.citations.map((c, i) => (
                      <li key={i}>
                        <a href={c.url} target="_blank" rel="noreferrer">
                          {c.title || c.url}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <textarea
        className="chat-input"
        placeholder="Ask about the data..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
          }
        }}
      />

      <button className="button-primary" onClick={sendMessage} disabled={loading}>
        {loading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}
