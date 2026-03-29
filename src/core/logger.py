class Logger:
    """
    Logger for tracking optimization steps and metrics.
    Stores logs as a list of dictionaries.
    """
    def __init__(self):
        self._logs = []

    def log_step(self, step, action, cost, distance, score, output, progress=None):
        entry = {
            'step': step,
            'action': action,
            'cost': cost,
            'distance': distance,
            'score': score,
            'progress': progress,
            'output': (output[:50] + '...') if isinstance(output, str) and len(output) > 50 else output
        }
        self._logs.append(entry)

    def get_logs(self):
        return list(self._logs)

    def reset(self):
        self._logs.clear()
