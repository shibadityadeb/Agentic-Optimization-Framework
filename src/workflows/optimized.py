import asyncio
from src.core.optimizer import choose_best_action
from src.core.distance import compute_distance

from src.agents import retriever, analyzer, decision

ACTION_MAP = {
    'retriever': retriever.run,
    'analyzer': analyzer.run,
    'decision': decision.run,
}

async def run_optimized(state):
    """
    Dynamically chooses and applies the best action at each step using the optimizer.
    Loops for a maximum of 5 steps or until convergence (distance < epsilon).
    Tracks token usage and step count. Returns the final state.
    """
    epsilon = 1.0
    max_steps = 5
    step = 0
    if not hasattr(state, "token_usage"):
        state.token_usage = 0
    while step < max_steps:
        # 1. Choose best action
        action_name = await choose_best_action(state, list(ACTION_MAP.keys()))
        action_fn = ACTION_MAP[action_name]
        # 2. Apply action
        state = await action_fn(state)
        # 3. Track steps
        if hasattr(state, "update_step"):
            state.update_step()
        # 4. Track token usage (if present)
        if hasattr(state, "token_usage"):
            pass  # already tracked in analyzer
        # 5. Check convergence
        dist = await compute_distance(state)
        if dist < epsilon:
            break
        step += 1
    return state
