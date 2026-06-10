# Keyvalue SSE Chat (React)

React training app with the same integration pattern from the slides:

- `src/streamChatResponse.ts` — POST + SSE stream parsing
- `src/useSSE.ts` — messages, streaming state, abort handling
- `src/components/ChatWidget.tsx` — floating chat bubble (bottom-right)

## Run locally

**Terminal 1 — API**

```bash
cd server
npm run dev
```

**Terminal 2 — React app**

```bash
cd client
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173), click the **chat bubble** on the right, and try:

`hello` → `react` → `how are you` → `who are you` → `thank you`

## Configure API URL

Default: `http://localhost:3001/events/stream`

Override with `.env`:

```
VITE_API_URL=https://your-deployed-api.onrender.com/events/stream
```

## Build

```bash
npm run build
npm run preview
```
