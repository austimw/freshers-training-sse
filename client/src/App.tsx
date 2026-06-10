import { ChatWidget } from "./components/ChatWidget";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <main className="app__content">
        <span className="app__badge">Training Demo</span>
        <h1>Keyvalue SSE Chat Integration</h1>
        <p>
          This page uses the same <code>streamChatResponse</code> and{" "}
          <code>useSSE</code> pattern from the training slides. Click the chat
          bubble on the right to talk to the bot.
        </p>
        <ul>
          <li>Start the API: <code>cd server && npm run dev</code></li>
          <li>Try prompts: hello, react, how are you, who are you, thank you</li>
        </ul>
      </main>

      <ChatWidget />
    </div>
  );
}
