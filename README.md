# Frontend Training — SSE & Chat Streaming

Static slide deck (PPT-style) for freshers: Server-Sent Events integration in React with TypeScript, focused on **POST + `fetch` streaming** for a chatbot UI.

## Preview locally

```bash
cd SSE-Freshers-training
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080)

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository.
2. **Settings → Pages → Build and deployment → Source:** Deploy from branch.
3. Branch: `main`, folder: `/` (root).
4. Your site will be at `https://<user>.github.io/<repo>/`

Ensure `assets/logo.png` is included in the repo.

## Contents (22 slides)

| # | Topic |
|---|--------|
| 1 | Title |
| 2–8 | SSE basics, format, EventSource, limits, vs WebSockets, use cases |
| 9–15 | Integration checklist, API contract, `streamChatResponse`, buffering, React, `useSSE`, chat UI |
| 16–19 | States, errors, reconnection, pitfalls |
| 20 | Practice + reveal solution |
| 21 | Mock streaming chat demo |
| 22 | Summary |

## Regenerate `index.html`

After editing slide content in `build_deck.py`:

```bash
python3 build_deck.py
```

Styles are copied from the reference training deck template.

## SSE Chatbot API (backend)

A Node/Express SSE server lives in [`server/`](server/). Students integrate against:

```
POST http://localhost:3001/events/stream
Body: { "content": "<user prompt>" }
Stream: data: {"content":"...","type":"delta"} lines, then [DONE]
```

Run locally:

```bash
cd server
npm install
npm run dev
```

**Test without building a React app:**

1. Terminal 1 — keep the API running (`npm run dev` in `server/`).
2. Terminal 2 — serve the slide deck:
   ```bash
   python3 -m http.server 8080
   ```
3. Open [http://localhost:8080](http://localhost:8080), go to slide **21 (Live Demo)**, type `hello`, and click **Send**.

Or use curl:

```bash
curl -N -X POST http://localhost:3001/events/stream \
  -H "Content-Type: application/json" \
  -d '{"content":"hello"}'
```

See [`server/README.md`](server/README.md) for supported prompts, curl examples, and Render deployment steps.

## React training app

A reference React implementation lives in [`client/`](client/) with `streamChatResponse`, `useSSE`, and a floating chat bubble UI.

```bash
# Terminal 1
cd server && npm run dev

# Terminal 2
cd client && npm install && npm run dev
```

Open [http://localhost:5173](http://localhost:5173) and click the chat bubble on the right.
