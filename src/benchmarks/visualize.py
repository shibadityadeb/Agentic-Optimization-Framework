import matplotlib.pyplot as plt
import os

def plot_cost_per_step(logs, label, out_path):
    steps = [entry['step'] for entry in logs]
    costs = [entry['cost'] for entry in logs]
    plt.figure()
    plt.plot(steps, costs, marker='o')
    plt.xlabel('Step')
    plt.ylabel('Cost')
    plt.title(f'Cost per Step ({label})')
    plt.savefig(out_path)
    plt.close()

def plot_distance_decay(logs, label, out_path):
    steps = [entry['step'] for entry in logs]
    distances = [entry['distance'] for entry in logs]
    plt.figure()
    plt.plot(steps, distances, marker='o')
    plt.xlabel('Step')
    plt.ylabel('Distance')
    plt.title(f'Distance Decay ({label})')
    plt.savefig(out_path)
    plt.close()

def plot_score_trend(logs, label, out_path):
    steps = [entry['step'] for entry in logs]
    scores = [entry['score'] for entry in logs]
    plt.figure()
    plt.plot(steps, scores, marker='o')
    plt.xlabel('Step')
    plt.ylabel('Score')
    plt.title(f'Score Trend ({label})')
    plt.savefig(out_path)
    plt.close()

def plot_steps_comparison(baseline_logs, optimized_logs, out_path):
    steps = [len(baseline_logs), len(optimized_logs)]
    labels = ['Baseline', 'Optimized']
    plt.figure()
    plt.bar(labels, steps)
    plt.ylabel('Total Steps')
    plt.title('Steps Comparison')
    plt.savefig(out_path)
    plt.close()
