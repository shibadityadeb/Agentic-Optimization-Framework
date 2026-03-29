import asyncio

from src.core.optimizer import choose_best_action
from src.core.distance import state_distance
from src.core.cost import compute_cost
from src.core.logger import Logger
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
    Tracks token usage and step count. Returns the final state and logs.
    """
    epsilon = 1.0
    max_steps = 5
    min_steps = 3
    step = 0
    logger = Logger()
    if not hasattr(state, "token_usage"):
        state.token_usage = 0
    prev_state = state.copy()
    from src.core.progress import compute_progress
    last_actions = []
    while step < max_steps:
        action_fns = list(ACTION_MAP.values())
        # 1. Choose best action and get score
        state._last_actions = last_actions
        best_action_fn, best_next_state, score = await choose_best_action(state, action_fns)
        # 2. Compute cost and distance (distance to previous state)
        cost = compute_cost(best_next_state, prev_state)
        distance = state_distance(best_next_state, prev_state)
        progress_val = compute_progress(best_next_state)
        # 3. Log step
        action_name = [k for k, v in ACTION_MAP.items() if v == best_action_fn][0]
        logger.log_step(step+1, action_name, cost, distance, score, getattr(best_next_state, 'output', ''), progress=progress_val)
        # 4. Print log line
        print(f"Step {step+1} | Action: {action_name} | Cost: {cost:.2f} | Dist: {distance:.2f} | Score: {score:.2f} | Progress: {progress_val:.2f}")
        # 5. Apply action
        prev_state = state
        state = await best_action_fn(state)
        # 6. Track steps
        if hasattr(state, "update_step"):
            state.update_step()
        # 7. Track last actions
        last_actions.append(action_name)
        if len(last_actions) > 5:
            last_actions = last_actions[-5:]
        # 8. Check convergence: at least min_steps, then check distance
        dist = state_distance(state, prev_state)
        step += 1
        if step >= min_steps and dist < epsilon:
            break
    return state, logger.get_logs()
