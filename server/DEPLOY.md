# Deploy the backend API (public endpoint)

Goal: get a URL like `https://keyvalue-sse-bot.onrender.com/events/stream` that students can call from anywhere.

Recommended host: **[Render](https://render.com)** (free tier, HTTPS included, works well with SSE).

---

## Step 1 — Push code to GitHub

This folder is not a git repo yet. From the project root:

```bash
cd SSE-Freshers-training

git init
git add .
git commit -m "Add SSE training deck, API server, and React client"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_ORG/SSE-Freshers-training.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Deploy on Render

1. Sign in at [render.com](https://render.com) (GitHub login is easiest).
2. **New +** → **Blueprint** (if you want to use `render.yaml`) **or** **Web Service**.
3. Connect the GitHub repo `SSE-Freshers-training`.

### Option A — Blueprint (uses `render.yaml` at repo root)

- Render reads `render.yaml` and creates the service automatically.
- Root directory, build, and health check are preconfigured.

### Option B — Manual Web Service

| Setting | Value |
|---------|--------|
| **Root Directory** | `server` |
| **Runtime** | Node |
| **Build Command** | `npm install && npm run build` |
| **Start Command** | `npm start` |
| **Health Check Path** | `/health` |

4. Choose **Free** instance type.
5. Click **Deploy**.

First deploy takes ~2–3 minutes.

---

## Step 3 — Copy your public endpoint

After deploy, Render gives you a URL, e.g.:

```
https://keyvalue-sse-bot.onrender.com
```

**Share this with students:**

```
POST https://keyvalue-sse-bot.onrender.com/events/stream
Content-Type: application/json

{ "content": "hello" }
```

Quick checks:

```bash
# Health
curl https://YOUR-URL.onrender.com/health

# SSE stream
curl -N -X POST https://YOUR-URL.onrender.com/events/stream \
  -H "Content-Type: application/json" \
  -d '{"content":"hello"}'
```

---

## Step 4 — Point the React app at the live API

Create `client/.env`:

```
VITE_API_URL=https://YOUR-URL.onrender.com/events/stream
```

Rebuild/restart the client after changing env vars.

---

## Free tier notes

| Topic | What to expect |
|-------|----------------|
| **Cold start** | Service sleeps after ~15 min idle. First request may take 30–60 s. |
| **HTTPS** | Included automatically (`https://...`) |
| **CORS** | Already enabled (`cors()` on all origins) — browsers can call from localhost or deployed frontends |
| **Cost** | $0 on Render free tier |

For training sessions, tell students: *“If the first message is slow, wait a moment and try again.”*

---

## Alternatives

| Platform | When to use |
|----------|-------------|
| **Railway** | Similar to Render; good if you already use it |
| **Fly.io** | More control, slightly more setup |
| **AWS / GCP** | Overkill for a demo API |

Avoid **Vercel/Netlify serverless** for this API — long-lived SSE streams are a poor fit there.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Build fails | Ensure **Root Directory** is `server`, not repo root |
| 502 on first request | Wait for cold start; check `/health` |
| CORS error in browser | API already allows all origins; confirm URL is `https` and path is `/events/stream` |
| Port error on Render | Do not hardcode 3001 — app uses `process.env.PORT` (already set up) |

---

## What students need (one line)

> API base: `https://YOUR-URL.onrender.com/events/stream`  
> Method: `POST` · Body: `{ "content": "hello" }` · Response: SSE stream ending with `[DONE]`
