import cors from "cors";
import express from "express";
import { SUPPORTED_PROMPTS } from "./bot/intents";
import { streamRouter } from "./routes/stream";

const app = express();
const port = Number(process.env.PORT) || 3001;

app.use(cors());
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({
    name: "Keyvalue SSE Chatbot API",
    endpoint: "POST /events/stream",
    body: { content: "hello" },
    supportedPrompts: SUPPORTED_PROMPTS.map((item) => ({
      examples: item.examples,
    })),
    health: "GET /health",
  });
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.use(streamRouter);

app.listen(port, () => {
  console.log(`Keyvalue SSE bot listening on http://localhost:${port}`);
});
