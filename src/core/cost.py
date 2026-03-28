from __future__ import annotations

from .distance import state_distance

ALPHA = 0.1
BETA = 0.1
GAMMA = 1.0
ETA = 0.5

DEFAULT_LATENCY = 1.0
ERROR_KEYWORD = "error"


def compute_cost(state, prev_state) -> float:
    """
    Compute cost for a transition from prev_state to state.

    Cost components:
    - token cost: length of output string
    - latency: constant placeholder for now
    - error: penalty if output contains the keyword 'error'
    - transition penalty: state distance

    Formula:
        c = alpha * tokens + beta * latency + gamma * error + eta * distance
    """
    output = getattr(state, "output", "")
    tokens = float(len(output))
    latency = DEFAULT_LATENCY
    error = 1.0 if ERROR_KEYWORD in output.lower() else 0.0
    distance = state_distance(state, prev_state)

    return (ALPHA * tokens) + (BETA * latency) + (GAMMA * error) + (ETA * distance)
