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
    stage = getattr(new_state, "steps", 0)

    if stage == 0:
        prompt = f"""
You are an expert financial analyst agent. Your task is to provide an initial rough analysis for the following query. Do NOT give a final answer or recommendation. Focus only on a high-level, preliminary assessment.

Query: {new_state.query}
Current Report:
{old_output}

Give only a rough, initial analysis. Do not provide a final recommendation yet.
"""
    elif stage == 1:
        prompt = f"""
You are an expert financial analyst agent. Refine the previous analysis for the following query. Add trends and risks, and improve the detail. Do NOT provide a final recommendation yet.

Query: {new_state.query}
Current Report:
{old_output}

Add trends and risks. Do not provide a final recommendation yet.
"""
    else:
        prompt = f"""
You are an expert financial analyst agent. Finalize the analysis for the following query. Complete the report and include a clear, actionable recommendation at the end.

Query: {new_state.query}
Current Report:
{old_output}

Finalize the analysis and provide a final recommendation.
"""
    response, tokens = await call_anthropic(prompt)
    if response.strip():
        new_state.output = response.strip()
    # Track token usage
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
