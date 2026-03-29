from __future__ import annotations

from typing import Any, Callable, Awaitable

from .cost import compute_cost
from .distance import state_distance
from .progress import compute_progress


# Scoring constants
LAMBDA = 0.5
MU = 0.5
RHO = 2.0

def score_fn(cost, distance, progress, progress_drop):
    return cost + (1.0 / LAMBDA) * distance - MU * progress + RHO * progress_drop


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


    # STEP 7: Agent selection logic
    # 1. If state.output is empty, force analyzer first
    if not getattr(state, 'output', ''):
        for a in actions:
            if a.__name__ == 'run' and hasattr(a, '__module__') and 'analyzer' in a.__module__:
                test_state = state.copy()
                test_state._last_actions = last_actions + ['analyzer.run']
                next_state = await a(test_state)
                cost = compute_cost(next_state, state)
                distance = state_distance(next_state, state)
                prog = compute_progress(next_state)
                progress_drop = max(0, 0 - prog)
                if distance == 0:
                    continue
                score = score_fn(cost, distance, prog, progress_drop)
                return a, next_state, score

    # 2. If output exists, remove retriever
    if getattr(state, 'output', ''):
        filtered_actions = []
        for a in actions:
            if not (a.__name__ == 'run' and hasattr(a, '__module__') and 'retriever' in a.__module__):
                filtered_actions.append(a)
        actions = filtered_actions

    prev_prog = compute_progress(state)
    last_action = last_actions[-1] if last_actions else None
    found_better = False
    for action in actions:
        action_name = action.__name__ + ('.' + action.__module__ if hasattr(action, '__module__') else '')
        # 3. Prevent repeating same action twice
        if last_action == action_name:
            continue
        test_state = state.copy()
        test_state._last_actions = last_actions + [action_name]
        next_state = await action(test_state)
        cost = compute_cost(next_state, state)
        distance = state_distance(next_state, state)
        prog = compute_progress(next_state)
        progress_drop = max(0, prev_prog - prog)
        # 10. Ensure non-zero distance
        if distance == 0:
            # Slightly modify output to ensure state change
            if hasattr(next_state, 'output'):
                next_state.output += " [minor update]"
                distance = 0.01
        score = score_fn(cost, distance, prog, progress_drop)
        if score < best_score:
            best_score = score
            best_action = action
            best_next_state = next_state
        if score < float('inf') and prog > prev_prog:
            found_better = True


    # Only force analyzer if no action improves score
    if not found_better:
        for a in actions:
            if a.__name__ == 'run' and hasattr(a, '__module__') and 'analyzer' in a.__module__:
                test_state = state.copy()
                test_state._last_actions = last_actions + ['analyzer.run']
                next_state = await a(test_state)
                cost = compute_cost(next_state, state)
                distance = state_distance(next_state, state)
                prog = compute_progress(next_state)
                progress_drop = max(0, prev_prog - prog)
                if distance == 0:
                    if hasattr(next_state, 'output'):
                        next_state.output += " [minor update]"
                        distance = 0.01
                score = score_fn(cost, distance, prog, progress_drop)
                if score < best_score:
                    best_score = score
                    best_action = a
                    best_next_state = next_state
                break

    # Always return finite score
    if best_action is None:
        # As a last resort, return analyzer
        for a in actions:
            if a.__name__ == 'run' and hasattr(a, '__module__') and 'analyzer' in a.__module__:
                test_state = state.copy()
                test_state._last_actions = last_actions + ['analyzer.run']
                next_state = await a(test_state)
                cost = compute_cost(next_state, state)
                distance = state_distance(next_state, state)
                prog = compute_progress(next_state)
                progress_drop = max(0, prev_prog - prog)
                if distance == 0:
                    if hasattr(next_state, 'output'):
                        next_state.output += " [minor update]"
                        distance = 0.01
                score = score_fn(cost, distance, prog, progress_drop)
                best_action = a
                best_next_state = next_state
                best_score = score
                break

    return best_action, best_next_state, best_score
