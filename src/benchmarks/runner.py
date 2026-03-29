import asyncio
from src.workflows.baseline import run_baseline
from src.workflows.optimized import run_optimized
from src.benchmarks.metrics import evaluate

def print_comparison(baseline_result, optimized_result, baseline_metrics, optimized_metrics):
    print("\n=== Benchmark Comparison ===")
    print(f"{'':<12} | {'Baseline':<15} | {'Optimized':<15}")
    print("-" * 45)
    print(f"{'Steps':<12} | {baseline_metrics['total_steps']:<15} | {optimized_metrics['total_steps']:<15}")
    print(f"{'Output':<12} | {str(baseline_result.get('output', ''))[:30]:<15} | {str(optimized_result.get('output', ''))[:30]:<15}")
    print(f"{'Cost':<12} | {baseline_metrics['cost']:<15} | {optimized_metrics['cost']:<15}")
    print("-" * 45)

async def run_benchmark():
    # 1. Create initial state
    initial_state = {
        'query': 'Analyze Tesla stock',
        'steps': 0,
        'output': ''
    }
    # 2. Run baseline workflow
    baseline_result = await run_baseline(initial_state.copy())
    # 3. Run optimized workflow
    optimized_result = await run_optimized(initial_state.copy())
    # 4. Evaluate both
    baseline_metrics = evaluate(baseline_result)
    optimized_metrics = evaluate(optimized_result)
    # 5. Print comparison
    print_comparison(baseline_result, optimized_result, baseline_metrics, optimized_metrics)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
