"""Test script for CI: run short rollouts to verify environment consistency."""
import argparse
import numpy as np
from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv


def test_rollout(task: str, episodes: int, max_steps: int):
    """Run test rollouts."""
    print(f"\nTesting {task} environment...")
    
    # Create environment
    if task == "pick_place":
        env = PickPlaceEnv(render_mode=None)
    elif task == "drawer":
        env = DrawerEnv(task_mode="open", render_mode=None)
    elif task == "button":
        env = ToolUseEnv(tool_type="button", render_mode=None)
    else:
        raise ValueError(f"Unknown task: {task}")
    
    success_count = 0
    total_steps = 0
    
    for ep in range(episodes):
        obs, info = env.reset(seed=ep)
        done = False
        steps = 0
        
        while not done and steps < max_steps:
            # Random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            steps += 1
        
        total_steps += steps
        if info.get("success", False):
            success_count += 1
        
        print(f"  Episode {ep+1}: steps={steps}, success={info.get('success', False)}")
    
    env.close()
    
    print(f"  Total steps: {total_steps}")
    print(f"  Success rate: {success_count}/{episodes}")
    print(f"  ✓ {task} environment test passed\n")
    
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=3)
    parser.add_argument("--max_steps", type=int, default=50)
    
    args = parser.parse_args()
    
    # Test all environments
    tasks = ["pick_place", "drawer", "button"]
    
    print("="*60)
    print("Running environment rollout tests for CI")
    print("="*60)
    
    all_passed = True
    for task in tasks:
        try:
            test_rollout(task, args.episodes, args.max_steps)
        except Exception as e:
            print(f"  ✗ {task} environment test FAILED: {e}\n")
            all_passed = False
    
    if all_passed:
        print("="*60)
        print("All tests passed! ✓")
        print("="*60)
    else:
        print("="*60)
        print("Some tests failed! ✗")
        print("="*60)
        exit(1)
