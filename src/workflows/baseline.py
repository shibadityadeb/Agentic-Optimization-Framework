from __future__ import annotations

from ..agents import analyzer, decision, retriever
from ..core.cost import compute_cost

def _increment_step(state):
    state.update_step()
    return state

async def run_baseline(state):
    current_state = state.copy()
    logs = []
    # Step 1: Retriever
    current_state = await retriever.run(current_state)
    _increment_step(current_state)
    cost1 = compute_cost(current_state, state)
    logs.append({'step': 1, 'action': 'retriever', 'cost': cost1})
    # Step 2: Analyzer
    prev_state = current_state.copy()
    current_state = await analyzer.run(current_state)
    _increment_step(current_state)
    cost2 = compute_cost(current_state, prev_state)
    logs.append({'step': 2, 'action': 'analyzer', 'cost': cost2})
    # Step 3: Decision
    prev_state = current_state.copy()
    current_state = await decision.run(current_state)
    _increment_step(current_state)
    cost3 = compute_cost(current_state, prev_state)
    logs.append({'step': 3, 'action': 'decision', 'cost': cost3})
    return current_state, logs
