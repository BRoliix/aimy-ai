from __future__ import annotations
import json
from typing import Dict, Any
from jinja2 import Template
from config.settings import settings
from src.services.openai_client import OpenAIClient


class AgentPipeline:
    """Minimal, prompt‑templated agent pipeline that can route to Aimy tools."""

    def __init__(self, tool_executor):
        self.tool_executor = tool_executor
        self.llm = OpenAIClient()
        # load template
        with open("prompts/assistant_system.j2", "r", encoding="utf-8") as f:
            self.system_template = Template(f.read())

    def run(self, user_text: str) -> Dict[str, Any]:
        system_prompt = self.system_template.render(
            model_name=settings.openai_model,
            tool_name=settings.tool_name,
            capabilities=settings.capabilities(),
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ]
        content = self.llm.chat(messages, temperature=0.2)
        # Try to parse as action JSON first
        action = self._parse_action(content)
        if action:
            # Execute tool via Aimy core
            tool_input = action.get("input", "").strip()
            tool_result = self.tool_executor(tool_input)
            return {
                "response": tool_result if isinstance(tool_result, str) else tool_result.get("message", str(tool_result)),
                "result": tool_result,
                "action_url": getattr(tool_result, "get", lambda *_: None)("web_url") if isinstance(tool_result, dict) else None,
            }
        # Otherwise return direct content
        return {"response": content, "result": {"type": "helpful_response"}}

    @staticmethod
    def _parse_action(text: str) -> Dict[str, Any] | None:
        s = text.strip()
        if not s:
            return None
        # If the model emitted JSON on a single line, parse it
        try:
            obj = json.loads(s)
            if isinstance(obj, dict) and obj.get("action") == "aimy_tool":
                return obj
        except Exception:
            pass
        return None
