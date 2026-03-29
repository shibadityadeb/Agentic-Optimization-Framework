import asyncio
from src.core.optimizer import choose_best_action
from src.core.distance import compute_distance
from src.agents.retriever import retrieve_action
from src.agents.analyzer import analyze_action
from src.agents.decision import decide_action

ACTIONS = {
    'retriever': retrieve_action,
    'analyzer': analyze_action,
    'decision': decide_action,
}

async def run_optimized(state):
    """
    Dynamically chooses and applies the best action at each step using the optimizer.
    Loops for a maximum of 5 steps or until convergence (distance < epsilon).
    Returns the final state.
    """
    epsilon = 1.0
    max_steps = 5
    step = 0
    
    while step < max_steps:
        # 1. Choose best action
        action_name = await choose_best_action(state, list(ACTIONS.keys()))
        action_fn = ACTIONS[action_name]
        # 2. Apply action
        state = await action_fn(state)
        # 3. Check convergence
        dist = await compute_distance(state)
        if dist < epsilon:
            break
        step += 1
    return state
