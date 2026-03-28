from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    if new_state.output:
        new_state.output = "final: " + new_state.output
    else:
        new_state.output = "final: no output"
    return new_state
