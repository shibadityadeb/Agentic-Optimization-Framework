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

async def run(state: "State") -> "State":
    new_state = state.copy()
    prompt = f"Query: {new_state.query}\nMemory: {', '.join(new_state.memory)}"
    try:
        output, tokens = await call_anthropic(prompt)
        new_state.output = output
        if not hasattr(new_state, "token_usage"):
            new_state.token_usage = 0
        new_state.token_usage += tokens
    except Exception as e:
        new_state.output = f"analysis error: {e}"
        if not hasattr(new_state, "token_usage"):
            new_state.token_usage = 0
    return new_state
