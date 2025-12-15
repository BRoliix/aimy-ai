from __future__ import annotations
from typing import Any

# Thin bridge to reuse existing AgenticAICore without deep refactors

def make_aimy_bridge(aimy_core):
    def executor(text: str) -> Any:
        # Delegate to existing process_request which can create content, open web, etc.
        return aimy_core.process_request(text)
    return executor
