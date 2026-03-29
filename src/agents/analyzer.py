from __future__ import annotations
import os
import asyncio
import httpx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")  # Use env or default

async def call_anthropic(prompt: str, max_tokens: int = 512) -> tuple[str, int]:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(ANTHROPIC_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        content = result["content"][0]["text"] if result.get("content") else ""
        usage = result.get("usage", {})
        total_tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
        return content, total_tokens

import random

async def run(state: "State") -> "State":
    new_state = state.copy()
    # Always produce or improve output
    if new_state.output:
        # Refine: add a new insight or improve
        refined = new_state.output
        words = refined.split()
        if len(words) > 5:
            idx = random.randint(0, len(words)-1)
            words[idx] = words[idx] + "*"  # Mark as improved
        refined = " ".join(words) + " [refined]"
        new_state.output = refined
        tokens = len(refined) // 4 + random.randint(2, 6)
    else:
        # First analysis: generate a longer output
        base = f"Initial analysis of: {new_state.query}. "
        base += "Key points: " + ", ".join(new_state.memory) if new_state.memory else "No memory."
        base += " [step1]"
        new_state.output = base
        tokens = len(base) // 4 + random.randint(5, 10)
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
