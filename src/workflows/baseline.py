from __future__ import annotations

from ..agents import analyzer, decision, retriever


def _increment_step(state):
    state.update_step()
    return state


async def run_baseline(state):
    current_state = state.copy()

    current_state = await retriever.run(current_state)
    _increment_step(current_state)

    current_state = await analyzer.run(current_state)
    _increment_step(current_state)

    current_state = await decision.run(current_state)
    _increment_step(current_state)

    return current_state
