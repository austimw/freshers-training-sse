export interface ChatRequestBody {
  content?: string;
}

export interface StreamDelta {
  content: string;
  type: "delta";
}
