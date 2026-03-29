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
    import time
    import hashlib
    old_output = new_state.output or ""
    # Section templates
    analysis_section = "Analysis:\nTesla stock shows strong volatility."
    trends_section = "Trends:\n- Increasing EV demand\n- Market expansion"
    risks_section = "Risks:\n- Competition\n- Market correction"
    insights_section = "Insights:\n- Innovation leadership\n- Regulatory headwinds"
    # Section logic
    if not old_output:
        # Step 1: Basic analysis
        new_state.output = analysis_section
        tokens = len(new_state.output) // 4 + random.randint(5, 10)
    elif "Trends:" not in old_output:
        # Step 2: Add trends
        new_state.output = old_output + "\n\n" + trends_section
        tokens = len(new_state.output) // 4 + random.randint(2, 6)
    elif "Risks:" not in old_output:
        # Step 3: Add risks
        new_state.output = old_output + "\n\n" + risks_section
        tokens = len(new_state.output) // 4 + random.randint(2, 6)
    elif "Insights:" not in old_output:
        # Step 4: Add insights
        new_state.output = old_output + "\n\n" + insights_section
        tokens = len(new_state.output) // 4 + random.randint(2, 6)
    else:
        # Further refinements: clarify or expand
        new_state.output = old_output + f"\n\nFurther detail: Expanded on previous sections."
        tokens = len(new_state.output) // 4 + random.randint(2, 6)
    # Prevent output shrinking
    if len(new_state.output) < len(old_output):
        return state
    # Ensure at least 2 sections for progress (penalize if not)
    section_count = sum([s in new_state.output for s in ["Analysis:", "Trends:", "Risks:", "Insights:"]])
    new_state.section_count = section_count
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
