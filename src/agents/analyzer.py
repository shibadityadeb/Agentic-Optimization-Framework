from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()
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
    old_output = new_state.output or ""
    # Compose a prompt for the LLM based on the current state
    prompt = f"""
You are an expert financial analyst agent. Your task is to analyze the following query and incrementally build a structured report. Each time you are called, you receive the current report so far. Add new insights, trends, risks, or analysis as appropriate, and never repeat content. If the report is already complete, refine or clarify it further.

Query: {new_state.query}
Current Report:


Respond with the next improved version of the report. Do not repeat previous content. Be concise and structured.
"""
    response, tokens = await call_anthropic(prompt)
    if response.strip():
        new_state.output = response.strip()
    # Track token usage
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
