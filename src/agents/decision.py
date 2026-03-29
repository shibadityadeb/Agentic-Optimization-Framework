from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    # Always improve output if possible
    if new_state.output:
        # Add a decision marker and a summary improvement
        new_state.output = f"final: {new_state.output} [decision improved]"
    else:
        new_state.output = "final: no output"
    return new_state
