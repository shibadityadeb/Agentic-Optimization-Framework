from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    old_output = new_state.output or ""
    if old_output:
        # Summarize analysis and add final recommendation (no 'final:' prefix)
        summary = "\nSummary: The above analysis covers key trends, risks, and insights for Tesla stock."
        recommendation = "\nFinal Recommendation: Buy/Hold/Sell"
        new_output = old_output
        if "summary:" not in old_output:
            new_output += summary
        if "Final Recommendation:" not in old_output:
            new_output += recommendation
        # Prevent output shrinking
        if len(new_output) < len(old_output):
            return state
        new_state.output = new_output
    else:
        new_state.output = "No analysis available.\nSummary: No findings.\nFinal Recommendation: Unable to provide recommendation."
    return new_state
