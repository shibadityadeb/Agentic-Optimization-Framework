from src.core.progress import compute_progress

class DummyState:
    def __init__(self, output):
        self.output = output

# Test cases
outputs = [
    "Analysis: Tesla stock shows strong volatility.",
    "Analysis: Tesla stock shows strong volatility.\nTrends: Increasing EV demand.",
    "Analysis: Tesla stock shows strong volatility.\nTrends: Increasing EV demand.\nRisks: Competition.\nFinal Recommendation: Buy"
]

for i, out in enumerate(outputs, 1):
    state = DummyState(out)
    print(f"Test {i} output: {out}")
    progress = compute_progress(state)
    print(f"Test {i} progress: {progress}")
    print("-"*40)
