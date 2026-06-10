const FALLBACK =
  "Sorry, I don't understand what you are saying.";

const RESPONSES = {
  welcome:
    "Hi! Welcome to the Keyvalue chatbot. What are you gonna learn today?",
  learn:
    "That's awesome! Frontend and streaming are a great combo. Want to try asking how your day is?",
  howAreYou:
    "I'm doing great, thanks for asking! Ready to help you practice SSE integration.",
  whoAreYou:
    "I'm the Keyvalue training bot — here to help you build your first streaming chat UI!",
  goodbye:
    "You're welcome! Good luck with your training — you've got this!",
} as const;

export function matchIntent(input: string): string {
  const msg = input.trim().toLowerCase();

  if (!msg) {
    return FALLBACK;
  }

  if (/^(hello|hi|hey)\b/.test(msg)) {
    return RESPONSES.welcome;
  }

  if (
    /\blearn\b/.test(msg) ||
    /\b(react|javascript|frontend|sse|typescript|js|ts)\b/.test(msg)
  ) {
    return RESPONSES.learn;
  }

  if (/how are you|how're you|hows it going|how's it going/.test(msg)) {
    return RESPONSES.howAreYou;
  }

  if (/who are you|what is your name|what's your name|your name/.test(msg)) {
    return RESPONSES.whoAreYou;
  }

  if (/^(bye|goodbye|thank you|thanks)\b/.test(msg)) {
    return RESPONSES.goodbye;
  }

  return FALLBACK;
}

export const SUPPORTED_PROMPTS = [
  { examples: ["hello", "hi", "hey"], reply: RESPONSES.welcome },
  {
    examples: ["react", "javascript", "frontend", "sse", "typescript"],
    reply: RESPONSES.learn,
  },
  { examples: ["how are you", "how's it going"], reply: RESPONSES.howAreYou },
  { examples: ["who are you", "what is your name"], reply: RESPONSES.whoAreYou },
  { examples: ["bye", "goodbye", "thank you", "thanks"], reply: RESPONSES.goodbye },
];
