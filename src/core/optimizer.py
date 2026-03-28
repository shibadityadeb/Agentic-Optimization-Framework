from __future__ import annotations

from typing import Any, Callable, Awaitable
from .cost import compute_cost
from .distance import state_distance

LAMBDA = 0.5


async def choose_best_action(state, actions: list[Callable[[Any], Awaitable[Any]]]):
    """
    For each action, simulate next state, compute cost and distance, and score.
    J = cost + (1/lambda) * distance
    Returns the action with the lowest score.
    Does not modify the original state.
    """
    best_score = float('inf')
    best_action = None
    best_next_state = None

    for action in actions:
        test_state = state.copy()
        next_state = await action(test_state)
        cost = compute_cost(next_state, state)
        distance = state_distance(next_state, state)
        score = cost + (1.0 / LAMBDA) * distance
        if score < best_score:
            best_score = score
            best_action = action
            best_next_state = next_state

    return best_action, best_next_state, best_score
