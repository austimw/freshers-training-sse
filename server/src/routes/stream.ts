import { Router } from "express";
import { matchIntent } from "../bot/intents";
import { streamReply } from "../bot/streamReply";
import type { ChatRequestBody } from "../types";

export const streamRouter = Router();

streamRouter.post("/events/stream", async (req, res) => {
  const body = req.body as ChatRequestBody;
  const content = typeof body.content === "string" ? body.content : "";
  const reply = matchIntent(content);

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  try {
    await streamReply(res, reply);
  } catch {
    if (!res.writableEnded) {
      res.end();
    }
  }
});
