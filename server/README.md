# Keyvalue SSE Chatbot API

Public SSE endpoint for frontend training students integrating a streaming chatbot with React.

## Quick start (local)

```bash
cd server
npm install
npm run dev
```

Server runs at `http://localhost:3001`.

## API

### `POST /events/stream`

**Request**

```http
POST /events/stream
Content-Type: application/json

{ "content": "hello" }
```

**Response** (`text/event-stream`)

```
data: {"content":"Hi!","type":"delta"}

data: {"content":"Hi! Welcome","type":"delta"}

...

data: [DONE]
```

Each `data:` line sends the next **token chunk**; your client accumulates them (same as the training slides).

### Supported prompts

Try these in your chat UI:

| # | Send something like | Bot reply |
|---|-------------------|-----------|
| 1 | `hello`, `hi`, `hey` | Welcome message |
| 2 | `react`, `javascript`, `frontend`, `sse`, `typescript` | Encouragement about learning |
| 3 | `how are you`, `how's it going` | Friendly status reply |
| 4 | `who are you`, `what is your name` | Bot introduction |
| 5 | `bye`, `goodbye`, `thank you`, `thanks` | Closing message |

Anything else → `Sorry, I don't understand what you are saying.`

### Test with curl

```bash
curl -N -X POST http://localhost:3001/events/stream \
  -H "Content-Type: application/json" \
  -d '{"content":"hello"}'
```

### Other routes

- `GET /` — API info and supported prompts
- `GET /health` — health check for deployment

## Connect from React

Point your `streamChatResponse` at this URL:

```typescript
const response = await fetch("https://YOUR-PUBLIC-URL/events/stream", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ content: prompt }),
  signal,
});
```

Locally:

```typescript
const response = await fetch("http://localhost:3001/events/stream", { ... });
```

## Deploy publicly

**Full guide:** [`DEPLOY.md`](DEPLOY.md)

Quick version:

1. Push this repo to GitHub.
2. [Render](https://render.com) → **New Web Service** (or **Blueprint** using root `render.yaml`).
3. **Root Directory:** `server` · **Build:** `npm install && npm run build` · **Start:** `npm start`
4. Share `https://YOUR-URL.onrender.com/events/stream` with students.

**Note:** Render free tier sleeps after inactivity. The first request after idle may take ~30 seconds.

## Production build

```bash
npm run build
npm start
```
