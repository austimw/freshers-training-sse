# Deploy the React web app

Production API (already live):

```
https://freshers-training-sse.onrender.com/events/stream
```

The app reads this from `client/.env.production` at build time.

---

## Deploy on Render (recommended — same account as the API)

1. Push latest code to GitHub.
2. Render Dashboard → **New +** → **Static Site**.
3. Connect repo `freshers-training-sse`.
4. Settings:

| Setting | Value |
|---------|--------|
| **Name** | `freshers-training-sse-web` |
| **Root Directory** | `client` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `dist` |

5. Add environment variable (optional if using `.env.production`):

| Key | Value |
|-----|--------|
| `VITE_API_URL` | `https://freshers-training-sse.onrender.com/events/stream` |

6. Deploy. Your URL will be something like:

```
https://freshers-training-sse-web.onrender.com
```

Or use **Blueprint** with the root `render.yaml` — it defines both the API and static site.

---

## Verify locally with production API

```bash
cd client
npm run build
npm run preview
```

Open the preview URL and test the chat bubble.

---

## Local dev (localhost API)

```bash
cp .env.example .env.local
npm run dev
```

Uses `http://localhost:3001/events/stream` from `.env.local` (or the default in `src/config.ts`).
