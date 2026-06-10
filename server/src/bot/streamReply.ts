import type { Response } from "express";
import type { StreamDelta } from "../types";

const CHUNK_DELAY_MS = 60;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function streamReply(res: Response, fullText: string): Promise<void> {
  const words = fullText.split(/\s+/).filter(Boolean);
  let accumulated = "";

  for (const word of words) {
    const chunk = (accumulated ? " " : "") + word;
    accumulated += chunk;
    const payload: StreamDelta = { content: chunk, type: "delta" };
    res.write(`data: ${JSON.stringify(payload)}\n\n`);
    await sleep(CHUNK_DELAY_MS);
  }

  res.write("data: [DONE]\n\n");
  res.end();
}
