import type { StreamDelta } from "./types";
import { API_URL } from "./config";

export async function streamChatResponse(
  prompt: string,
  onStreamData: (text: string, type?: string) => void,
  signal?: AbortSignal
): Promise<string> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: prompt }),
    signal,
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let done = false;
  let buffer = "";
  let accumulatedText = "";

  while (!done) {
    const { value, done: readerDone } = await reader.read();
    done = readerDone;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      if (trimmed === "data: [DONE]" || trimmed === "[DONE]") {
        return accumulatedText;
      }

      if (trimmed.startsWith("data:")) {
        try {
          const json = JSON.parse(
            trimmed.replace(/^data:\s*/, "")
          ) as StreamDelta;
          if (json.content) {
            accumulatedText += json.content;
            onStreamData(accumulatedText, json.type);
          }
        } catch (err) {
          console.error("Parse error", err);
        }
      }
    }
  }

  return accumulatedText;
}
