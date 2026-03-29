def evaluate(state):
    """
    Evaluate the given state and return metrics.
    Returns a dict with:
      - total_steps: Number of steps taken (expects 'steps' in state)
      - output_length: Length of output (expects 'output' in state)
      - cost: Simple cost estimate (steps * output_length)
    """
    total_steps = state.get('steps', 0)
    output = state.get('output', "")
    output_length = len(output) if isinstance(output, str) else 0
    cost = total_steps * output_length
    return {
        'total_steps': total_steps,
        'output_length': output_length,
        'cost': cost
    }
