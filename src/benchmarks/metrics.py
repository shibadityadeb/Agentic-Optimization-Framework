def evaluate(state):
    """
    Evaluate the given state and return metrics.
    Returns a dict with:
      - total_steps: Number of steps taken (expects 'steps' in state)
      - output_length: Length of output (expects 'output' in state)
      - token_usage: Real token usage (if available)
      - cost: Improved cost estimate (steps * output_length + token_usage)
    """
    total_steps = getattr(state, 'steps', 0)
    output = getattr(state, 'output', "")
    output_length = len(output) if isinstance(output, str) else 0
    token_usage = getattr(state, 'token_usage', 0)
    cost = total_steps * output_length + token_usage
    return {
        'total_steps': total_steps,
        'output_length': output_length,
        'token_usage': token_usage,
        'cost': cost
    }
