import { FormEvent, useEffect, useRef, useState } from "react";
import { useSSE } from "../useSSE";
import "./ChatWidget.css";

export function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const { messages, isStreaming, error, sendMessage, clearMessages } = useSSE();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (open) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, open, isStreaming]);

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
    }
  }, [open]);

  const handleSubmit = async (event?: FormEvent) => {
    event?.preventDefault();
    const prompt = input.trim();
    if (!prompt || isStreaming) return;
    setInput("");
    await sendMessage(prompt);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSubmit();
    }
  };

  return (
    <div className="chat-widget">
      {open && (
        <div className="chat-panel" role="dialog" aria-label="Keyvalue chatbot">
          <header className="chat-panel__header">
            <div>
              <h2>Keyvalue Bot</h2>
              <p>SSE streaming demo</p>
            </div>
            <div className="chat-panel__actions">
              <button
                type="button"
                className="chat-icon-btn"
                onClick={clearMessages}
                aria-label="Clear chat"
                title="Clear chat"
              >
                ↺
              </button>
              <button
                type="button"
                className="chat-icon-btn"
                onClick={() => setOpen(false)}
                aria-label="Close chat"
                title="Close"
              >
                ✕
              </button>
            </div>
          </header>

          <div className="chat-panel__messages">
            {messages.length === 0 && (
              <div className="chat-empty">
                <p>Say hello to get started.</p>
                <p className="chat-empty__hint">
                  Try: hello, react, how are you, who are you, thank you
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`chat-bubble chat-bubble--${message.role}`}
              >
                <span className="chat-bubble__role">
                  {message.role === "user" ? "You" : "Bot"}
                </span>
                <p>{message.text || (isStreaming ? "…" : "")}</p>
              </div>
            ))}

            {isStreaming && (
              <div className="chat-typing">Bot is typing…</div>
            )}

            {error && <div className="chat-error">{error}</div>}

            <div ref={messagesEndRef} />
          </div>

          <form className="chat-panel__input" onSubmit={handleSubmit}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a message…"
              rows={2}
              disabled={isStreaming}
            />
            <button type="submit" disabled={!input.trim() || isStreaming}>
              Send
            </button>
          </form>
        </div>
      )}

      <button
        type="button"
        className={`chat-fab ${open ? "chat-fab--open" : ""}`}
        onClick={() => setOpen((prev) => !prev)}
        aria-label={open ? "Close chat" : "Open chat"}
        aria-expanded={open}
      >
        {open ? "✕" : "💬"}
      </button>
    </div>
  );
}
