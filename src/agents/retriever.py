from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state import State


async def run(state: "State") -> "State":
    new_state = state.copy()
    new_state.memory.append("data fetched")
    return new_state
