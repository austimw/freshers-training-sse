#!/usr/bin/env python3
"""Generate index.html for SSE Frontend Training deck."""

from pathlib import Path

ROOT = Path(__file__).parent
head = (ROOT / "_styles_head.txt").read_text()
head = head.replace(
    "<title>Immutability, Closures & Callbacks — JavaScript Training</title>",
    "<title>SSE &amp; Chat Streaming — Frontend Training</title>",
)

extra_css = """
        .compare-table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: .82rem; }
        .compare-table th, .compare-table td { border: 1px solid var(--border); padding: 10px 14px; text-align: left; }
        .compare-table th { background: var(--surface-2); color: var(--accent-light); font-weight: 600; }
        .compare-table tr:nth-child(even) td { background: var(--surface); }
        .chat-demo { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px; }
        .chat-panel { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; display: flex; flex-direction: column; min-height: 260px; }
        .chat-panel h3 { margin-top: 0; font-size: 1rem; }
        .chat-messages { flex: 1; overflow-y: auto; background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 12px; font-size: .82rem; margin-bottom: 10px; min-height: 120px; }
        .chat-msg { margin-bottom: 10px; }
        .chat-msg.user { color: var(--cyan); }
        .chat-msg.bot { color: var(--green); }
        .chat-msg .role { font-weight: 700; font-size: .7rem; text-transform: uppercase; letter-spacing: 1px; }
        .chat-input-row { display: flex; gap: 8px; }
        .chat-input-row textarea { flex: 1; min-height: 48px; padding: 10px 12px; border-radius: 8px; border: 1px solid var(--border); background: var(--code-bg); color: var(--text); font-family: 'Inter', sans-serif; font-size: .82rem; }
        .demo-btn { background: var(--accent); color: #fff; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; font-family: 'Inter', sans-serif; font-size: .8rem; }
        .demo-btn:hover { background: var(--accent-light); }
        .demo-btn:disabled { opacity: .4; cursor: default; }
        .status-pill { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: .72rem; font-weight: 600; margin-bottom: 8px; }
        .status-idle { background: var(--surface-2); color: var(--text-dim); }
        .status-streaming { background: var(--info-bg); color: var(--accent-light); border: 1px solid var(--accent); }
        .status-done { background: var(--output-bg); color: var(--green); border: 1px solid var(--green); }
        .status-error { background: rgba(248,113,113,.1); color: var(--red); border: 1px solid var(--red); }
        @media (max-width: 900px) { .chat-demo { grid-template-columns: 1fr; } }
"""
head = head.replace("    </style>", extra_css + "    </style>")

slides_html = r'''
<div id="deck">

    <section class="slide" data-title="Welcome">
        <div class="slide-label">Frontend Training Session</div>
        <h1>Frontend Training &mdash; SSE &amp; Chat Streaming</h1>
        <p class="dim" style="font-size:1.05rem; margin-top:8px;">Complete frontend integration of Server-Sent Events in React — from protocol basics to a streaming chatbot.</p>
        <div style="margin-top:32px; display:flex; gap:14px; flex-wrap:wrap;">
            <span class="tag-pill">SSE</span>
            <span class="tag-pill">EventSource</span>
            <span class="tag-pill">fetch + ReadableStream</span>
            <span class="tag-pill">TypeScript</span>
            <span class="tag-pill">useSSE</span>
        </div>
        <p class="dim" style="margin-top:40px;font-size:.78rem;">Use <span class="inline-code">Arrow Keys</span> or the buttons below to navigate &bull; Press <span class="inline-code">M</span> for menu</p>
    </section>

    <section class="slide" data-title="Why Real-Time?">
        <div class="slide-label">Introduction</div>
        <h2>Why Real-Time on the Web?</h2>
        <p>Traditional HTTP: the client asks, the server answers <strong>once</strong>. For a chatbot, waiting for the full reply feels slow.</p>
        <div class="card-grid" style="margin-top:18px;">
            <div class="card">
                <h3>Without streaming</h3>
                <ul>
                    <li>User sends a prompt</li>
                    <li>Spinner for several seconds</li>
                    <li>Full answer appears at once</li>
                </ul>
            </div>
            <div class="card">
                <h3>With SSE / stream</h3>
                <ul>
                    <li>User sends a prompt</li>
                    <li>Tokens arrive <span class="highlight">incrementally</span></li>
                    <li>UI updates like ChatGPT typing</li>
                </ul>
            </div>
        </div>
        <div class="info-box"><strong>Goal today:</strong> integrate a <span class="inline-code">POST</span> streaming API in React so bot messages render token-by-token.</div>
    </section>

    <section class="slide" data-title="What is SSE?">
        <div class="slide-label">Introduction</div>
        <h2>What is Server-Sent Events (SSE)?</h2>
        <p><span class="highlight">SSE</span> is a standard way for a server to <strong>push data to the browser</strong> over a single HTTP connection.</p>
        <ul style="margin-top:14px;">
            <li><strong>Direction:</strong> server &rarr; client only (one-way)</li>
            <li><strong>Transport:</strong> plain HTTP</li>
            <li><strong>Content-Type:</strong> <span class="inline-code">text/event-stream</span></li>
            <li><strong>Format:</strong> text lines the client parses (<span class="inline-code">data:</span>, <span class="inline-code">event:</span>, etc.)</li>
        </ul>
        <div class="ref-diagram" style="margin-top:18px;">
            Browser &nbsp;&larr;&mdash;&mdash; continuous stream &mdash;&mdash;&nbsp; Server<br>
            <span class="dim">(one HTTP connection stays open)</span>
        </div>
    </section>

    <section class="slide" data-title="SSE Message Format">
        <div class="slide-label">Protocol</div>
        <h2>SSE Message Format</h2>
        <p>Each event is a block of lines ending with a <strong>blank line</strong>.</p>
        <pre><code><span class="cmt">// Example stream from server</span>
event: token
data: {"content":"Hello","type":"delta"}

event: token
data: {"content":" world","type":"delta"}

data: [DONE]
</code></pre>
        <div class="cols">
            <div>
                <h3>Common fields</h3>
                <ul>
                    <li><span class="inline-code">data:</span> payload (required)</li>
                    <li><span class="inline-code">event:</span> event name (optional)</li>
                    <li><span class="inline-code">id:</span> for reconnection</li>
                    <li><span class="inline-code">retry:</span> reconnect delay (ms)</li>
                </ul>
            </div>
            <div>
                <h3>Multiline data</h3>
                <pre><code>data: line one
data: line two

<span class="cmt">// Received as: "line one\nline two"</span></code></pre>
            </div>
        </div>
    </section>

    <section class="slide" data-title="EventSource API">
        <div class="slide-label">EventSource (~20%)</div>
        <h2>EventSource in 5 Minutes</h2>
        <p>The browser ships a built-in API for <strong>GET</strong> SSE endpoints.</p>
        <pre><code><span class="kw">const</span> source = <span class="kw">new</span> <span class="fn">EventSource</span>(<span class="str">'/api/notifications'</span>);

source.<span class="fn">onopen</span> = () =&gt; console.<span class="fn">log</span>(<span class="str">'connected'</span>);
source.<span class="fn">onmessage</span> = (event) =&gt; {
  console.<span class="fn">log</span>(<span class="str">'data:'</span>, event.data);
};
source.<span class="fn">onerror</span> = () =&gt; console.<span class="fn">log</span>(<span class="str">'error / reconnecting'</span>);

<span class="cmt">// Named events</span>
source.<span class="fn">addEventListener</span>(<span class="str">'order-update'</span>, (event) =&gt; {
  <span class="kw">const</span> payload = JSON.<span class="fn">parse</span>(event.data);
});

<span class="cmt">// Cleanup</span>
source.<span class="fn">close</span>();</code></pre>
        <div class="info-box"><strong>Good for:</strong> live feeds, dashboards, notifications — simple GET subscriptions.</div>
    </section>

    <section class="slide" data-title="EventSource Limits">
        <div class="slide-label">EventSource</div>
        <h2>EventSource Limitations</h2>
        <p>Why our <strong>chatbot</strong> usually does <em>not</em> stop at <span class="inline-code">EventSource</span>:</p>
        <div class="card-grid">
            <div class="card">
                <h3 class="danger">GET only</h3>
                <p>Cannot send a JSON body with the user prompt.</p>
            </div>
            <div class="card">
                <h3 class="danger">No custom headers</h3>
                <p>Cannot set <span class="inline-code">Authorization</span> (in the standard API).</p>
            </div>
            <div class="card">
                <h3 class="warn">Less control</h3>
                <p>You rely on browser parsing; harder to abort mid-stream from app logic.</p>
            </div>
            <div class="card">
                <h3 class="highlight">Auto-reconnect</h3>
                <p>Browser reconnects and can send <span class="inline-code">Last-Event-ID</span> — a real pro!</p>
            </div>
        </div>
        <div class="info-box"><strong>Chat pattern:</strong> <span class="inline-code">POST</span> prompt in body &rarr; stream tokens back &rarr; use <span class="inline-code">fetch</span> + <span class="inline-code">ReadableStream</span>.</div>
    </section>

    <section class="slide" data-title="SSE vs WebSockets">
        <div class="slide-label">Comparison</div>
        <h2>SSE vs WebSockets</h2>
        <table class="compare-table">
            <tr><th></th><th>SSE</th><th>WebSockets</th></tr>
            <tr><td>Direction</td><td>Server &rarr; client</td><td>Both ways</td></tr>
            <tr><td>Protocol</td><td>HTTP</td><td>WS (upgrade)</td></tr>
            <tr><td>Data format</td><td>Text (UTF-8)</td><td>Text or binary</td></tr>
            <tr><td>Reconnect</td><td>Built-in (EventSource)</td><td>Manual</td></tr>
            <tr><td>Complexity</td><td>Lower</td><td>Higher</td></tr>
            <tr><td>Great for</td><td>Feeds, logs, <strong>LLM streaming</strong></td><td>Games, chat rooms, collab editing</td></tr>
        </table>
        <p class="dim" style="margin-top:10px;">Many chat UIs use HTTP streaming (SSE-style) or WebSockets — pick based on bidirectional needs and infra.</p>
    </section>

    <section class="slide" data-title="When to Use SSE">
        <div class="slide-label">Use Cases</div>
        <h2>When to Use SSE in Frontend</h2>
        <div class="cols">
            <div>
                <h3 class="highlight">Good fits</h3>
                <ul>
                    <li>AI / chatbot token streaming</li>
                    <li>Live notifications &amp; alerts</li>
                    <li>Dashboard metrics</li>
                    <li>Progress bars (builds, uploads)</li>
                    <li>Live sports scores / tickers</li>
                </ul>
            </div>
            <div>
                <h3 class="warn">Consider WebSockets instead</h3>
                <ul>
                    <li>Low-latency two-way gaming</li>
                    <li>Collaborative editors (ops both ways)</li>
                    <li>Binary data (audio/video frames)</li>
                    <li>Many messages per second both directions</li>
                </ul>
            </div>
        </div>
    </section>

    <section class="slide" data-title="Integration Checklist">
        <div class="slide-label">Integration</div>
        <h2>Frontend Integration Checklist</h2>
        <div class="card-grid">
            <div class="card"><h3>1. Contract</h3><p>URL, method, body shape, event format, end signal.</p></div>
            <div class="card"><h3>2. Connect</h3><p><span class="inline-code">fetch</span> or <span class="inline-code">EventSource</span> — open the stream.</p></div>
            <div class="card"><h3>3. Parse</h3><p>Split chunks into lines; read <span class="inline-code">data:</span> payloads.</p></div>
            <div class="card"><h3>4. Update UI</h3><p>Append tokens to React state via callback/hook.</p></div>
            <div class="card"><h3>5. Errors</h3><p>Network, HTTP status, JSON parse failures.</p></div>
            <div class="card"><h3>6. Cleanup</h3><p><span class="inline-code">AbortController</span>, <span class="inline-code">close()</span>, avoid duplicate connections.</p></div>
        </div>
    </section>

    <section class="slide" data-title="API Contract">
        <div class="slide-label">Integration</div>
        <h2>API Contract — Chat Bot</h2>
        <p>Example backend our React app expects (you will implement the server later):</p>
        <pre><code><span class="cmt">// Request</span>
POST /events/stream
Content-Type: application/json

{ <span class="str">"content"</span>: <span class="str">"Explain SSE in one sentence"</span> }

<span class="cmt">// Response (stream)</span>
Content-Type: text/event-stream

data: {"content":"Server","type":"delta"}
data: {"content":"-Sent","type":"delta"}
data: {"content":" Events","type":"delta"}
data: [DONE]</code></pre>
        <div class="ref-diagram">User prompt &rarr; POST &rarr; Server streams <span class="inline-code">data:</span> lines &rarr; UI grows message</div>
    </section>

    <section class="slide" data-title="fetch Stream">
        <div class="slide-label">Integration — fetch (~80%)</div>
        <h2>Step 1 — <span class="inline-code">streamChatResponse</span></h2>
        <p>Service function: POST the prompt, read the body as a stream, parse SSE lines.</p>
        <pre><code><span class="kw">export async function</span> <span class="fn">streamChatResponse</span>(
  prompt: <span class="kw">string</span>,
  onStreamData: (text: <span class="kw">string</span>, type?: <span class="kw">string</span>) =&gt; <span class="kw">void</span>,
  signal?: AbortSignal
): <span class="kw">Promise</span>&lt;<span class="kw">string</span>&gt; {
  <span class="kw">const</span> response = <span class="kw">await</span> <span class="fn">fetch</span>(<span class="str">'http://localhost:3001/events/stream'</span>, {
    method: <span class="str">'POST'</span>,
    headers: { <span class="str">'Content-Type'</span>: <span class="str">'application/json'</span> },
    body: JSON.<span class="fn">stringify</span>({ content: prompt }),
    signal,
  });

  <span class="kw">if</span> (!response.ok) <span class="kw">throw new</span> <span class="fn">Error</span>(<span class="str">`HTTP ${response.status}`</span>);
  <span class="kw">if</span> (!response.body) <span class="kw">throw new</span> <span class="fn">Error</span>(<span class="str">'No response body'</span>);

  <span class="kw">const</span> reader = response.body.<span class="fn">getReader</span>();
  <span class="kw">const</span> decoder = <span class="kw">new</span> <span class="fn">TextDecoder</span>(<span class="str">'utf-8'</span>);
  <span class="kw">let</span> done = <span class="kw">false</span>;
  <span class="kw">let</span> buffer = <span class="str">''</span>;
  <span class="kw">let</span> accumulatedText = <span class="str">''</span>;

  <span class="kw">while</span> (!done) {
    <span class="kw">const</span> { value, done: readerDone } = <span class="kw">await</span> reader.<span class="fn">read</span>();
    done = readerDone;
    buffer += decoder.<span class="fn">decode</span>(value, { stream: <span class="kw">true</span> });
    <span class="cmt">// parse lines from buffer (see next slide)</span>
  }
  <span class="kw">return</span> accumulatedText;
}</code></pre>
    </section>

    <section class="slide" data-title="Line Buffering">
        <div class="slide-label">Integration — fetch</div>
        <h2>Step 2 — Chunk &amp; Line Buffering</h2>
        <p>One <span class="inline-code">read()</span> may end mid-line. Buffer incomplete data before parsing.</p>
        <pre><code><span class="kw">const</span> lines = buffer.<span class="fn">split</span>(<span class="str">'\n'</span>);
buffer = lines.<span class="fn">pop</span>() ?? <span class="str">''</span>; <span class="cmt">// keep incomplete last line</span>

<span class="kw">for</span> (<span class="kw">const</span> line <span class="kw">of</span> lines) {
  <span class="kw">const</span> trimmed = line.<span class="fn">trim</span>();
  <span class="kw">if</span> (!trimmed) <span class="kw">continue</span>;
  <span class="kw">if</span> (trimmed === <span class="str">'[DONE]'</span>) <span class="kw">break</span>;

  <span class="kw">if</span> (trimmed.<span class="fn">startsWith</span>(<span class="str">'data:'</span>)) {
    <span class="kw">try</span> {
      <span class="kw">const</span> json = JSON.<span class="fn">parse</span>(trimmed.<span class="fn">replace</span>(<span class="str">'data: '</span>, <span class="str">''</span>));
      <span class="kw">if</span> (json.content) {
        accumulatedText += json.content;
        <span class="fn">onStreamData</span>(accumulatedText, json.type);
      }
    } <span class="kw">catch</span> (err) {
      console.<span class="fn">error</span>(<span class="str">'Parse error'</span>, err);
    }
  }
}</code></pre>
        <div class="info-box"><strong>Common bug:</strong> splitting the whole buffer without saving the last partial line → broken JSON.</div>
    </section>

    <section class="slide" data-title="React Pattern">
        <div class="slide-label">React</div>
        <h2>Step 3 — Keep Streaming Out of JSX</h2>
        <div class="cols">
            <div>
                <h3 class="danger">Avoid</h3>
                <ul>
                    <li>Parsing stream inside <span class="inline-code">render</span></li>
                    <li>Mutating DOM directly</li>
                    <li>Creating a new connection every render</li>
                </ul>
            </div>
            <div>
                <h3 class="highlight">Do</h3>
                <ul>
                    <li>Service: <span class="inline-code">streamChatResponse</span></li>
                    <li>Hook: connection state + messages</li>
                    <li>UI: render state only</li>
                </ul>
            </div>
        </div>
        <pre><code><span class="cmt">// Component — thin UI layer</span>
<span class="kw">const</span> { messages, isStreaming, error, sendMessage } = <span class="fn">useSSE</span>();

<span class="kw">return</span> (
  &lt;ChatWindow
    messages={messages}
    loading={isStreaming}
    error={error}
    onSend={sendMessage}
  /&gt;
);</code></pre>
    </section>

    <section class="slide" data-title="useSSE Hook">
        <div class="slide-label">React</div>
        <h2>Step 4 — <span class="inline-code">useSSE</span> Hook</h2>
        <pre><code><span class="kw">import</span> { useCallback, useRef, useState } from <span class="str">'react'</span>;
<span class="kw">import</span> { streamChatResponse } from <span class="str">'./streamChatResponse'</span>;

<span class="kw">export function</span> <span class="fn">useSSE</span>() {
  <span class="kw">const</span> [messages, setMessages] = useState&lt;ChatMessage[]&gt;([]);
  <span class="kw">const</span> [isStreaming, setIsStreaming] = useState(<span class="kw">false</span>);
  <span class="kw">const</span> [error, setError] = useState&lt;<span class="kw">string</span> | <span class="kw">null</span>&gt;(<span class="kw">null</span>);
  <span class="kw">const</span> abortRef = useRef&lt;AbortController | <span class="kw">null</span>&gt;(<span class="kw">null</span>);

  <span class="kw">const</span> sendMessage = <span class="fn">useCallback</span>(<span class="kw">async</span> (prompt: <span class="kw">string</span>) =&gt; {
    abortRef.current?.<span class="fn">abort</span>();
    abortRef.current = <span class="kw">new</span> <span class="fn">AbortController</span>();
    setError(<span class="kw">null</span>);
    setIsStreaming(<span class="kw">true</span>);

    setMessages((prev) =&gt; [...prev,
      { role: <span class="str">'user'</span>, text: prompt },
      { role: <span class="str">'assistant'</span>, text: <span class="str">''</span> },
    ]);

    <span class="kw">try</span> {
      <span class="kw">await</span> <span class="fn">streamChatResponse</span>(prompt, (accumulated) =&gt; {
        setMessages((prev) =&gt; {
          <span class="kw">const</span> next = [...prev];
          next[next.length - <span class="num">1</span>] = { role: <span class="str">'assistant'</span>, text: accumulated };
          <span class="kw">return</span> next;
        });
      }, abortRef.current.signal);
    } <span class="kw">catch</span> (e) {
      <span class="kw">if</span> ((e <span class="kw">as</span> Error).name !== <span class="str">'AbortError'</span>) {
        setError((e <span class="kw">as</span> Error).message);
      }
    } <span class="kw">finally</span> {
      setIsStreaming(<span class="kw">false</span>);
    }
  }, []);

  <span class="kw">return</span> { messages, isStreaming, error, sendMessage };
}</code></pre>
    </section>

    <section class="slide" data-title="Chat UI Wiring">
        <div class="slide-label">React</div>
        <h2>Step 5 — Wire to Chat UI</h2>
        <pre><code><span class="kw">function</span> <span class="fn">ChatPage</span>() {
  <span class="kw">const</span> { messages, isStreaming, error, sendMessage } = <span class="fn">useSSE</span>();
  <span class="kw">const</span> [input, setInput] = useState(<span class="str">''</span>);

  <span class="kw">const</span> handleSubmit = () =&gt; {
    <span class="kw">if</span> (!input.trim() || isStreaming) <span class="kw">return</span>;
    sendMessage(input.trim());
    setInput(<span class="str">''</span>);
  };

  <span class="kw">return</span> (
    &lt;div&gt;
      {messages.map((m, i) =&gt; (
        &lt;p key={i}&gt;&lt;strong&gt;{m.role}:&lt;/strong&gt; {m.text}&lt;/p&gt;
      ))}
      {isStreaming &amp;&amp; &lt;span&gt;Bot is typing...&lt;/span&gt;}
      {error &amp;&amp; &lt;p className="error"&gt;{error}&lt;/p&gt;}
      &lt;textarea value={input} onChange={(e) =&gt; setInput(e.target.value)} /&gt;
      &lt;button onClick={handleSubmit} disabled={isStreaming}&gt;Send&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
        <div class="info-box">Update the <strong>last assistant message</strong> on each chunk — that produces the typing effect.</div>
    </section>

    <section class="slide" data-title="Connection States">
        <div class="slide-label">Reliability</div>
        <h2>Connection States in the UI</h2>
        <div class="card-grid">
            <div class="card"><h3>idle</h3><p>Ready for input. Enable send button.</p></div>
            <div class="card"><h3>connecting / streaming</h3><p>Disable send; show typing indicator.</p></div>
            <div class="card"><h3>done</h3><p>Stream finished (<span class="inline-code">[DONE]</span> or connection closed).</p></div>
            <div class="card"><h3>error</h3><p>Show message + optional Retry button.</p></div>
        </div>
        <pre><code><span class="kw">type</span> StreamStatus = <span class="str">'idle'</span> | <span class="str">'streaming'</span> | <span class="str">'done'</span> | <span class="str">'error'</span>;</code></pre>
        <p class="dim">Map <span class="inline-code">isStreaming</span> + <span class="inline-code">error</span> from the hook to labels users understand.</p>
    </section>

    <section class="slide" data-title="Error Handling">
        <div class="slide-label">Reliability</div>
        <h2>Error Handling</h2>
        <ul>
            <li><strong>HTTP errors:</strong> check <span class="inline-code">response.ok</span> before reading the body</li>
            <li><strong>Network drop:</strong> <span class="inline-code">fetch</span> rejects — catch and show UI message</li>
            <li><strong>Parse errors:</strong> bad JSON line — log and skip line (don’t crash the stream)</li>
            <li><strong>User navigates away:</strong> <span class="inline-code">AbortController.abort()</span></li>
            <li><strong>New prompt while streaming:</strong> abort previous request first</li>
        </ul>
        <pre><code><span class="kw">try</span> {
  <span class="kw">await</span> <span class="fn">streamChatResponse</span>(prompt, onChunk, signal);
} <span class="kw">catch</span> (err) {
  <span class="kw">if</span> ((err <span class="kw">as</span> Error).name === <span class="str">'AbortError'</span>) <span class="kw">return</span>;
  setError(err instanceof Error ? err.message : <span class="str">'Stream failed'</span>);
}</code></pre>
    </section>

    <section class="slide" data-title="Reconnection">
        <div class="slide-label">Reliability</div>
        <h2>Reconnection Strategies</h2>
        <div class="cols">
            <div class="card">
                <h3>EventSource</h3>
                <ul>
                    <li>Browser auto-reconnects</li>
                    <li>Sends <span class="inline-code">Last-Event-ID</span> header</li>
                    <li>Server can resume from <span class="inline-code">id:</span></li>
                </ul>
            </div>
            <div class="card">
                <h3>fetch stream (chat)</h3>
                <ul>
                    <li>No auto-reconnect — you implement it</li>
                    <li>Exponential backoff: 1s, 2s, 4s…</li>
                    <li>Max retries, then show “Failed — Retry”</li>
                    <li>Often <strong>don’t</strong> resume mid-answer — restart prompt</li>
                </ul>
            </div>
        </div>
        <div class="info-box">For chatbots, retry usually means <strong>re-send the prompt</strong>, not resume half a token.</div>
    </section>

    <section class="slide" data-title="Production Pitfalls">
        <div class="slide-label">Reliability</div>
        <h2>Production Pitfalls</h2>
        <ul>
            <li><span class="danger">Duplicate connections</span> — missing cleanup in <span class="inline-code">useEffect</span> / Strict Mode</li>
            <li><span class="danger">Not aborting</span> — user sends twice → two streams fight over state</li>
            <li><span class="warn">Forgetting <span class="inline-code">reader.releaseLock()</span></span> in advanced cases</li>
            <li><span class="warn">Line buffer bugs</span> — corrupted JSON from chunk boundaries</li>
            <li><span class="warn">Updating wrong message index</span> in the messages array</li>
        </ul>
        <pre><code><span class="fn">useEffect</span>(() =&gt; {
  <span class="kw">return</span> () =&gt; abortRef.current?.<span class="fn">abort</span>();
}, []);</code></pre>
    </section>

    <section class="slide" data-title="Practice Assignment">
        <div class="slide-label">Practice Time</div>
        <h2>Assignment — Build <span class="inline-code">useSSE</span></h2>
        <div class="assignment-card">
            <h3>Your task</h3>
            <ol>
                <li>Create <span class="inline-code">streamChatResponse.ts</span> with POST + stream parsing.</li>
                <li>Create <span class="inline-code">useSSE.ts</span> with messages, <span class="inline-code">isStreaming</span>, <span class="inline-code">error</span>, <span class="inline-code">sendMessage</span>.</li>
                <li>Render a simple chat UI that shows tokens arriving incrementally.</li>
            </ol>
        </div>
        <button class="reveal-btn" onclick="toggleReveal('reveal-sse')">Reveal Code</button>
        <div id="reveal-sse" class="hidden-code">
            <pre><code><span class="cmt">// streamChatResponse.ts — core loop</span>
<span class="kw">export async function</span> <span class="fn">streamChatResponse</span>(
  prompt: <span class="kw">string</span>,
  onStreamData: (text: <span class="kw">string</span>, type?: <span class="kw">string</span>) =&gt; <span class="kw">void</span>,
  signal?: AbortSignal
): <span class="kw">Promise</span>&lt;<span class="kw">string</span>&gt; {
  <span class="kw">const</span> res = <span class="kw">await</span> <span class="fn">fetch</span>(<span class="str">'http://localhost:3001/events/stream'</span>, {
    method: <span class="str">'POST'</span>,
    headers: { <span class="str">'Content-Type'</span>: <span class="str">'application/json'</span> },
    body: JSON.<span class="fn">stringify</span>({ content: prompt }),
    signal,
  });
  <span class="kw">if</span> (!res.ok || !res.body) <span class="kw">throw new</span> <span class="fn">Error</span>(<span class="str">'Stream failed'</span>);
  <span class="kw">const</span> reader = res.body.<span class="fn">getReader</span>();
  <span class="kw">const</span> decoder = <span class="kw">new</span> <span class="fn">TextDecoder</span>();
  <span class="kw">let</span> buffer = <span class="str">''</span>, acc = <span class="str">''</span>, done = <span class="kw">false</span>;
  <span class="kw">while</span> (!done) {
    <span class="kw">const</span> { value, done: d } = <span class="kw">await</span> reader.<span class="fn">read</span>();
    done = d;
    buffer += decoder.<span class="fn">decode</span>(value, { stream: <span class="kw">true</span> });
    <span class="kw">const</span> lines = buffer.<span class="fn">split</span>(<span class="str">'\n'</span>);
    buffer = lines.<span class="fn">pop</span>() ?? <span class="str">''</span>;
    <span class="kw">for</span> (<span class="kw">const</span> line <span class="kw">of</span> lines) {
      <span class="kw">if</span> (line.trim() === <span class="str">'[DONE]'</span>) <span class="kw">return</span> acc;
      <span class="kw">if</span> (line.<span class="fn">startsWith</span>(<span class="str">'data:'</span>)) {
        <span class="kw">const</span> json = JSON.<span class="fn">parse</span>(line.replace(<span class="str">'data: '</span>, <span class="str">''</span>));
        <span class="kw">if</span> (json.content) { acc += json.content; <span class="fn">onStreamData</span>(acc, json.type); }
      }
    }
  }
  <span class="kw">return</span> acc;
}</code></pre>
        </div>
    </section>

    <section class="slide" data-title="Live Demo">
        <div class="slide-label">Try It</div>
        <h2>Live Demo — Keyvalue Chatbot</h2>
        <p class="dim" style="margin-bottom:8px;">Streams from <span class="inline-code">http://localhost:3001/events/stream</span> — start the server with <span class="inline-code">cd server && npm run dev</span>.</p>
        <div class="chat-demo">
            <div class="chat-panel">
                <h3>Chat UI</h3>
                <span id="demo-status" class="status-pill status-idle">idle</span>
                <div id="demo-messages" class="chat-messages"></div>
                <div class="chat-input-row">
                    <textarea id="demo-input" placeholder="Try: hello, react, how are you..."></textarea>
                    <button class="demo-btn" id="demo-send" onclick="runLiveStream()">Send</button>
                </div>
            </div>
            <div class="chat-panel">
                <h3>What happens</h3>
                <ul style="font-size:.82rem;">
                    <li>POST to <span class="inline-code">/events/stream</span> with your prompt</li>
                    <li>Server streams <span class="inline-code">data:</span> chunks token-by-token</li>
                    <li>UI updates the last bot message as tokens arrive</li>
                </ul>
                <button class="demo-btn" style="margin-top:12px;" onclick="clearMockChat()">Clear chat</button>
            </div>
        </div>
    </section>

    <section class="slide" data-title="Summary">
        <div class="slide-label">Wrap Up</div>
        <h2>Summary</h2>
        <div class="card-grid">
            <div class="card">
                <h3>SSE basics</h3>
                <ul>
                    <li>One-way server &rarr; client over HTTP</li>
                    <li>Text format: <span class="inline-code">data:</span>, <span class="inline-code">event:</span>, <span class="inline-code">[DONE]</span></li>
                    <li><span class="inline-code">EventSource</span> for simple GET feeds</li>
                </ul>
            </div>
            <div class="card">
                <h3>Chat integration</h3>
                <ul>
                    <li><span class="inline-code">fetch</span> + <span class="inline-code">ReadableStream</span> for POST</li>
                    <li>Buffer lines across chunks</li>
                    <li><span class="inline-code">useSSE</span> + abort on unmount</li>
                </ul>
            </div>
            <div class="card">
                <h3>Next step</h3>
                <ul>
                    <li>Implement backend stream</li>
                    <li>Point URL to real API</li>
                    <li>Swap mock demo for live stream</li>
                </ul>
            </div>
        </div>
        <div style="text-align:center;margin-top:24px;">
            <p style="font-size:1.1rem;color:var(--accent-light);font-weight:600;">Thank you! Happy coding!</p>
            <p class="dim" style="margin-top:6px;font-size:.82rem;">
                <a href="https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events" style="color:var(--cyan);">MDN — SSE</a>
                &nbsp;&bull;&nbsp;
                <a href="https://developer.mozilla.org/en-US/docs/Web/API/EventSource" style="color:var(--cyan);">MDN — EventSource</a>
            </p>
        </div>
    </section>

</div>
'''

footer = r'''
<div id="nav-bar">
    <button id="btn-prev" onclick="navigate(-1)">&#8592; Previous</button>
    <span id="slide-counter">1 / 22</span>
    <button id="btn-next" onclick="navigate(1)">Next &#8594;</button>
</div>

<script>
    const slides = document.querySelectorAll('.slide');
    const total = slides.length;
    let current = 0;
    const CHAT_API_URL = 'http://localhost:3001/events/stream';
    let demoAbort = null;

    function showSlide(index) {
        slides.forEach((s, i) => {
            s.classList.remove('active', 'exit-left');
            if (i < index) s.classList.add('exit-left');
        });
        slides[index].classList.add('active');
        document.getElementById('slide-counter').textContent = `${index + 1} / ${total}`;
        document.getElementById('progress').style.width = `${((index + 1) / total) * 100}%`;
        document.getElementById('btn-prev').disabled = index === 0;
        document.getElementById('btn-next').disabled = index === total - 1;
        updateToc();
    }

    function navigate(dir) {
        const next = current + dir;
        if (next < 0 || next >= total) return;
        current = next;
        showSlide(current);
    }

    function goToSlide(index) {
        current = index;
        showSlide(current);
        closeToc();
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); navigate(1); }
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); navigate(-1); }
        if (e.key === 'm' || e.key === 'M') toggleToc();
        if (e.key === 'Escape') closeToc();
    });

    function buildToc() {
        const list = document.getElementById('toc-list');
        slides.forEach((s, i) => {
            const li = document.createElement('li');
            li.textContent = `${i + 1}. ${s.dataset.title}`;
            li.onclick = () => goToSlide(i);
            list.appendChild(li);
        });
    }

    function updateToc() {
        document.querySelectorAll('#toc li').forEach((li, i) => {
            li.classList.toggle('active', i === current);
        });
    }

    function toggleToc() {
        document.getElementById('toc').classList.toggle('open');
    }

    function closeToc() {
        document.getElementById('toc').classList.remove('open');
    }

    function toggleReveal(id) {
        const block = document.getElementById(id);
        const btn = block.previousElementSibling;
        const showing = block.classList.toggle('visible');
        btn.textContent = showing ? 'Hide Code' : 'Reveal Code';
    }

    let darkLogoSrc = null;

    function getTheme() {
        return document.documentElement.getAttribute('data-theme');
    }

    function toggleTheme() {
        const next = getTheme() === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        document.getElementById('theme-toggle').innerHTML = next === 'dark' ? '&#9790;' : '&#9728;';
        updateWatermark();
    }

    function buildDarkLogo(callback) {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = function () {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const d = imageData.data;
            for (let i = 0; i < d.length; i += 4) {
                const r = d[i], g = d[i+1], b = d[i+2];
                const max = Math.max(r, g, b);
                const min = Math.min(r, g, b);
                const sat = max === 0 ? 0 : (max - min) / max;
                if (r > 248 && g > 248 && b > 248) {
                    d[i+3] = 0;
                } else if (r > 220 && g > 220 && b > 220 && sat < 0.06) {
                    const w = (r + g + b) / (3 * 255);
                    d[i+3] = Math.round(255 * (1 - w));
                }
            }
            ctx.putImageData(imageData, 0, 0);
            darkLogoSrc = canvas.toDataURL('image/png');
            callback();
        };
        img.src = 'assets/logo.png';
    }

    function updateWatermark() {
        const wm = document.getElementById('watermark');
        if (!wm) return;
        wm.src = getTheme() === 'dark' && darkLogoSrc ? darkLogoSrc : 'assets/logo.png';
    }

    function injectWatermark() {
        const wm = document.createElement('img');
        wm.id = 'watermark';
        wm.className = 'watermark';
        wm.alt = '';
        wm.draggable = false;
        wm.src = 'assets/logo.png';
        document.body.appendChild(wm);
        buildDarkLogo(updateWatermark);
    }

    function setDemoStatus(status) {
        const el = document.getElementById('demo-status');
        el.className = 'status-pill status-' + status;
        el.textContent = status;
    }

    function appendDemoMessage(role, text) {
        const box = document.getElementById('demo-messages');
        const div = document.createElement('div');
        div.className = 'chat-msg ' + (role === 'user' ? 'user' : 'bot');
        div.innerHTML = '<div class="role">' + role + '</div><div class="msg-text"></div>';
        div.querySelector('.msg-text').textContent = text;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
        return div;
    }

    function clearMockChat() {
        if (demoAbort) demoAbort.abort();
        document.getElementById('demo-messages').innerHTML = '';
        setDemoStatus('idle');
        document.getElementById('demo-send').disabled = false;
    }

    async function streamChatResponse(prompt, onStreamData, signal) {
        const response = await fetch(CHAT_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: prompt }),
            signal,
        });

        if (!response.ok) throw new Error('HTTP ' + response.status);
        if (!response.body) throw new Error('No response body');

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let done = false;
        let buffer = '';
        let accumulatedText = '';

        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            buffer += decoder.decode(value, { stream: true });

            const lines = buffer.split('\n');
            buffer = lines.pop() ?? '';

            for (const line of lines) {
                const trimmed = line.trim();
                if (!trimmed) continue;
                if (trimmed === 'data: [DONE]' || trimmed === '[DONE]') return accumulatedText;

                if (trimmed.startsWith('data:')) {
                    try {
                        const json = JSON.parse(trimmed.replace(/^data:\s*/, ''));
                        if (json.content) {
                            accumulatedText += json.content;
                            onStreamData(accumulatedText, json.type);
                        }
                    } catch (err) {
                        console.error('Parse error', err);
                    }
                }
            }
        }

        return accumulatedText;
    }

    async function runLiveStream() {
        const input = document.getElementById('demo-input');
        const prompt = input.value.trim();
        if (!prompt) return;

        const sendBtn = document.getElementById('demo-send');
        sendBtn.disabled = true;
        if (demoAbort) demoAbort.abort();
        demoAbort = new AbortController();

        appendDemoMessage('user', prompt);
        input.value = '';
        const botEl = appendDemoMessage('assistant', '');
        const botText = botEl.querySelector('.msg-text');
        const messagesBox = document.getElementById('demo-messages');
        setDemoStatus('streaming');

        try {
            await streamChatResponse(prompt, (accumulated) => {
                botText.textContent = accumulated;
                messagesBox.scrollTop = messagesBox.scrollHeight;
            }, demoAbort.signal);
            setDemoStatus('done');
        } catch (err) {
            if (err.name === 'AbortError') {
                setDemoStatus('idle');
            } else {
                botText.textContent = err.message || 'Stream failed — is the server running?';
                setDemoStatus('error');
            }
        } finally {
            sendBtn.disabled = false;
        }
    }

    document.getElementById('theme-toggle').innerHTML = getTheme() === 'dark' ? '&#9790;' : '&#9728;';
    buildToc();
    showSlide(0);
    injectWatermark();
</script>
</body>
</html>
'''

body_mid = '''
<div id="progress"></div>
<div class="top-bar-backdrop"></div>
<button id="toc-toggle" onclick="toggleToc()">&#9776;</button>
<button id="theme-toggle" onclick="toggleTheme()" title="Toggle light / dark mode">&#9790;</button>
<nav id="toc"><h4>Contents</h4><ul id="toc-list"></ul></nav>
<div id="toc-overlay" onclick="toggleToc()"></div>
'''

html = head.replace('</head>', '')  # head ends with </style></head> from file
# _styles_head ends at </style> only - check
if '</head>' not in head:
    html = head + '\n</head>\n<body>\n' + body_mid + slides_html + footer
else:
    html = head.replace('</head>', '</head>\n<body>\n' + body_mid) + slides_html + footer

(ROOT / 'index.html').write_text(html)
print('Wrote index.html,', len(html), 'bytes, slides:', html.count('class="slide"'))