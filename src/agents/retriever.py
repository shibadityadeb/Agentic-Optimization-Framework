from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    # Compose a prompt for the LLM to simulate data retrieval
    prompt = f"""
You are a data retrieval agent. Your job is to fetch and summarize relevant data for the following query. Provide a concise, structured summary of the most important facts or statistics that would help an analyst.

Query: {new_state.query}

Respond with a data summary only. Do not include analysis or recommendations.
"""
    from .analyzer import call_anthropic
    response, tokens = await call_anthropic(prompt)
    if response.strip():
        new_state.memory.append(response.strip())
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
