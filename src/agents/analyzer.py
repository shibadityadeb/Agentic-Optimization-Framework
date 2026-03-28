from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    if new_state.memory:
        new_state.output = "analysis: " + ", ".join(new_state.memory)
    else:
        new_state.output = "analysis: no data"
    return new_state
