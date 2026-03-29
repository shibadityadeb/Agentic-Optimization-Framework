from __future__ import annotations

from typing import Any, Callable, Awaitable
from .cost import compute_cost
from .distance import state_distance


LAMBDA = 0.5
MU = 0.05

def progress(state):
    return len(getattr(state, 'output', ''))


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

    # Track last actions for constraint logic
    last_actions = getattr(state, '_last_actions', [])

    # If output is empty, force analyzer
    if not getattr(state, 'output', ''):
        forced_action = None
        for a in actions:
            if a.__name__ == 'run' and hasattr(a, '__module__') and 'analyzer' in a.__module__:
                forced_action = a
                break
        if forced_action:
            test_state = state.copy()
            next_state = await forced_action(test_state)
            cost = compute_cost(next_state, state)
            distance = state_distance(next_state, state)
            prog = progress(next_state)
            score = cost + (1.0 / LAMBDA) * distance - MU * prog
            return forced_action, next_state, score

    # Prevent repeating same action >2 times
    for action in actions:
        action_name = action.__name__ + ('.' + action.__module__ if hasattr(action, '__module__') else '')
        if len(last_actions) >= 2 and last_actions[-1] == last_actions[-2] == action_name:
            continue
        test_state = state.copy()
        # Pass last_actions to next state for tracking
        test_state._last_actions = last_actions + [action_name]
        next_state = await action(test_state)
        cost = compute_cost(next_state, state)
        distance = state_distance(next_state, state)
        prog = progress(next_state)
        score = cost + (1.0 / LAMBDA) * distance - MU * prog
        if score < best_score:
            best_score = score
            best_action = action
            best_next_state = next_state

    # If all actions are blocked by repeat constraint, allow any
    if best_action is None:
        for action in actions:
            test_state = state.copy()
            next_state = await action(test_state)
            cost = compute_cost(next_state, state)
            distance = state_distance(next_state, state)
            prog = progress(next_state)
            score = cost + (1.0 / LAMBDA) * distance - MU * prog
            if score < best_score:
                best_score = score
                best_action = action
                best_next_state = next_state

    return best_action, best_next_state, best_score
