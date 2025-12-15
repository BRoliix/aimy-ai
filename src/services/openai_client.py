from __future__ import annotations
from typing import List, Dict, Any
from openai import OpenAI
from config.settings import settings


class OpenAIClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.model = model or settings.openai_model
        self._client = OpenAI(api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        msg = resp.choices[0].message
        # message may have .content or .tool_calls; we only need content here
        return (msg.content or "").strip()
