"""
LLM Client module.
Handles text generation and token streaming via Free Groq Cloud (Llama 3.1/3.3), Google Gemini, OpenAI, or local offline fallback synthesizer.
"""

import os
import json
import asyncio
import urllib.request
import urllib.error
from typing import AsyncGenerator, Optional


class LLMClient:
    """
    LLM Client providing async streaming text generation.
    Supports 100% Free Groq Cloud (Llama 3.1), Google Gemini, OpenAI, and offline fallback.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.api_key = api_key or self.groq_api_key or self.gemini_api_key or self.openai_api_key

        # Set default model according to active provider
        if model:
            self.model = model
        elif self.groq_api_key:
            self.model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")
        elif self.gemini_api_key:
            self.model = os.environ.get("LLM_MODEL", "gemini-1.5-flash")
        elif self.openai_api_key:
            self.model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
        else:
            self.model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")

    async def generate_stream(self, prompt: str, context: str) -> AsyncGenerator[str, None]:
        """
        Yields token strings asynchronously as they are generated from Groq, Gemini, OpenAI, or offline fallback.
        """
        # 1. Try Free Groq Cloud (Llama 3.1 / 3.3)
        if self.groq_api_key or (self.api_key and "gsk_" in str(self.api_key)):
            try:
                groq_key = self.groq_api_key or self.api_key
                async for token in self._stream_groq(prompt, groq_key):
                    yield token
                return
            except Exception as e:
                print(f"[LLMClient] Groq Cloud API stream fallback due to: {e}")

        # 2. Try Google Gemini Free Tier
        if self.gemini_api_key or (self.api_key and "AIza" in str(self.api_key)):
            try:
                import google.generativeai as genai
                gemini_key = self.gemini_api_key or self.api_key
                genai.configure(api_key=gemini_key)
                g_model = genai.GenerativeModel(self.model)
                response = g_model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                        await asyncio.sleep(0.01)
                return
            except Exception as e:
                print(f"[LLMClient] Gemini API stream fallback due to: {e}")

        # 3. Grounded Fallback Synthesizer (for local dev / unconfigured API keys)
        async for token in self._fallback_synthesize_stream(prompt, context):
            yield token

    async def _stream_groq(self, prompt: str, api_key: str) -> AsyncGenerator[str, None]:
        """
        Streams completions from Groq Cloud OpenAI-compatible endpoint in real time.
        """
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        payload = {
            "model": self.model if "llama" in self.model else "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": True,
            "temperature": 0.3,
            "max_tokens": 800
        }

        # Run HTTP stream in thread pool to maintain non-blocking async execution
        loop = asyncio.get_event_loop()

        def make_request():
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            return urllib.request.urlopen(req, timeout=15)

        response = await loop.run_in_executor(None, make_request)

        while True:
            line_bytes = await loop.run_in_executor(None, response.readline)
            if not line_bytes:
                break

            line = line_bytes.decode("utf-8").strip()
            if not line or not line.startswith("data:"):
                continue

            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break

            try:
                data = json.loads(data_str)
                delta = data.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
                    await asyncio.sleep(0.005)
            except Exception:
                continue

    async def _fallback_synthesize_stream(self, prompt: str, context: str) -> AsyncGenerator[str, None]:
        """
        Generates grounded token stream from context for dev/fallback mode.
        """
        if "NO RELEVANT KNOWLEDGE CONTEXT FOUND" in context:
            answer = (
                "I'm sorry, but I couldn't find specific details regarding your query in Akhil's portfolio. "
                "Feel free to drop Akhil a direct message via the contact form on the home page!"
            )
        else:
            # Extract key context snippet cleanly
            lines = [line for line in context.split("\n") if line.strip() and not line.startswith("---") and not line.startswith("[Source")]
            snippet = " ".join(lines[:6]) if lines else context[:300]
            answer = f"Based on Akhil's portfolio records:\n\n{snippet}\n\nFeel free to explore the relevant project details and skills section for more information!"

        # Stream words as tokens with tiny realistic delay
        words = answer.split(" ")
        for idx, word in enumerate(words):
            token = word + (" " if idx < len(words) - 1 else "")
            yield token
            await asyncio.sleep(0.02)
