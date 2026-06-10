export interface ChatMessage {
  role: "user" | "assistant";
  text: string;
}

export interface StreamDelta {
  content: string;
  type?: string;
}
