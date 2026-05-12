"""Visualize evaluation results."""
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def plot_results(results_path: str):
    """Plot evaluation metrics from JSON results."""
    with open(results_path, 'r') as f:
        data = json.load(f)
    
    episodes = data['episodes']
    
    # Extract metrics
    ep_nums = [ep['episode'] for ep in episodes]
    successes = [ep['success'] for ep in episodes]
    steps = [ep['steps'] for ep in episodes]
    rewards = [ep['reward'] for ep in episodes]
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Success rate over episodes
    ax = axes[0, 0]
    success_rate = np.cumsum(successes) / (np.arange(len(successes)) + 1) * 100
    ax.plot(ep_nums, success_rate, linewidth=2)
    ax.axhline(data['success_rate'] * 100, color='r', linestyle='--', label='Final')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Cumulative Success Rate')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Steps per episode
    ax = axes[0, 1]
    ax.plot(ep_nums, steps, alpha=0.6, linewidth=1)
    ax.axhline(data['avg_steps'], color='r', linestyle='--', label='Average')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Steps')
    ax.set_title('Steps to Completion')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Reward per episode
    ax = axes[1, 0]
    ax.plot(ep_nums, rewards, alpha=0.6, linewidth=1)
    ax.axhline(data['avg_reward'], color='r', linestyle='--', label='Average')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reward')
    ax.set_title('Episode Reward')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Success distribution
    ax = axes[1, 1]
    success_counts = [sum(successes), len(successes) - sum(successes)]
    ax.pie(success_counts, labels=['Success', 'Failure'], autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c'], startangle=90)
    ax.set_title('Success Distribution')
    
    plt.tight_layout()
    
    # Save figure
    output_path = Path(results_path).parent / f"{Path(results_path).stem}_plot.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    
    plt.show()


def print_summary(results_path: str):
    """Print summary statistics."""
    with open(results_path, 'r') as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Total Episodes: {len(data['episodes'])}")
    print(f"Success Rate: {data['success_rate']*100:.1f}%")
    print(f"Average Steps: {data['avg_steps']:.1f}")
    print(f"Average Reward: {data['avg_reward']:.2f}")
    
    # Additional statistics
    episodes = data['episodes']
    successful_eps = [ep for ep in episodes if ep['success']]
    
    if successful_eps:
        avg_success_steps = np.mean([ep['steps'] for ep in successful_eps])
        print(f"Average Steps (Success): {avg_success_steps:.1f}")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=str, required=True, help="Path to results JSON")
    parser.add_argument("--no-plot", action="store_true", help="Skip plotting")
    
    args = parser.parse_args()
    
    print_summary(args.results)
    
    if not args.no_plot:
        try:
            plot_results(args.results)
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
