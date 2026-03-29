

import asyncio
import json
import os
import pandas as pd
from src.workflows.baseline import run_baseline
from src.workflows.optimized import run_optimized
from src.benchmarks.metrics import evaluate
from src.benchmarks.visualize import (
    plot_cost_per_step, plot_distance_decay, plot_score_trend, plot_steps_comparison
)
from src.core.state import State

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
LOGS_PATH = os.path.join(DATA_DIR, 'logs.json')
CSV_PATH = os.path.join(DATA_DIR, 'metrics.csv')
COST_PNG = os.path.join(DATA_DIR, 'cost.png')
DIST_PNG = os.path.join(DATA_DIR, 'distance.png')
SCORE_PNG = os.path.join(DATA_DIR, 'score.png')
STEPS_PNG = os.path.join(DATA_DIR, 'steps.png')

def print_comparison(baseline_steps, optimized_steps, baseline_cost, optimized_cost, baseline_out_len, optimized_out_len):
    print("\n=== Benchmark Comparison ===")
    print(f"Steps: {baseline_steps} vs {optimized_steps}")
    print(f"Total Cost: {baseline_cost} vs {optimized_cost}")
    print(f"Final Output Length: {baseline_out_len} vs {optimized_out_len}")
    print("-----------------------------------")

async def run_benchmark():
    # 1. Create initial state as State object
    initial_state = State(query='Analyze Tesla stock', steps=0, output='')
    # 2. Run baseline workflow
    baseline_state, baseline_logs = await run_baseline(initial_state.copy())
    # 3. Run optimized workflow
    optimized_state, optimized_logs = await run_optimized(initial_state.copy())
    # 4. Evaluate both
    baseline_metrics = evaluate(baseline_state)
    optimized_metrics = evaluate(optimized_state)

    # 5. Save logs
    logs_dict = {"baseline": baseline_logs, "optimized": optimized_logs}
    with open(LOGS_PATH, 'w') as f:
        json.dump(logs_dict, f, indent=2)

    # 6. Export CSV
    rows = []
    for log in baseline_logs:
        row = log.copy()
        row['workflow_type'] = 'baseline'
        # Fill missing fields for baseline logs
        for k in ['distance', 'score']:
            if k not in row:
                row[k] = None
        rows.append(row)
    for log in optimized_logs:
        row = log.copy()
        row['workflow_type'] = 'optimized'
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)

    # 7. Visualization
    if optimized_logs:
        plot_cost_per_step(optimized_logs, 'Optimized', COST_PNG)
        plot_distance_decay(optimized_logs, 'Optimized', DIST_PNG)
        plot_score_trend(optimized_logs, 'Optimized', SCORE_PNG)
    if baseline_logs and optimized_logs:
        plot_steps_comparison(baseline_logs, optimized_logs, STEPS_PNG)

    # 8. Print final summary
    print_comparison(
        len(baseline_logs), len(optimized_logs),
        baseline_metrics['cost'], optimized_metrics['cost'],
        baseline_metrics['output_length'], optimized_metrics['output_length']
    )

if __name__ == "__main__":
    asyncio.run(run_benchmark())
