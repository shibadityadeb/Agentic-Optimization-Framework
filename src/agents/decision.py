from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    old_output = new_state.output or ""
    # Compose a prompt for the LLM to generate a summary and recommendation
    prompt = f"""
You are a decision-making agent. Given the following structured analysis report, generate a concise summary and a final actionable recommendation (e.g., Buy, Hold, Sell, or similar). If the analysis is incomplete, state so clearly.

Analysis Report:
{old_output}

Respond with a summary and a final recommendation. Be clear and direct.
"""
    from .analyzer import call_anthropic
    response, tokens = await call_anthropic(prompt)
    if response.strip():
        new_state.output = response.strip()
    if not hasattr(new_state, "token_usage"):
        new_state.token_usage = 0
    new_state.token_usage += tokens
    return new_state
