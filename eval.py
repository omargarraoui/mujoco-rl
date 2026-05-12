"""Evaluation script for trained policies."""
import argparse
import torch
import numpy as np
from tqdm import tqdm
import json
import os
import imageio

from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv
from policies.mlp_policy import MLPPolicy
from policies.rnn_policy import RNNPolicy


def evaluate_policy(args):
    """Evaluate trained policy."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create environment
    if args.task == "pick_place":
        env = PickPlaceEnv(render_mode="rgb_array" if args.render else None)
    elif args.task == "drawer":
        env = DrawerEnv(task_mode="open", render_mode="rgb_array" if args.render else None)
    elif args.task == "button":
        env = ToolUseEnv(tool_type="button", render_mode="rgb_array" if args.render else None)
    else:
        raise ValueError(f"Unknown task: {args.task}")
    
    # Load policy
    if args.policy_type == "mlp":
        policy = MLPPolicy(
            action_dim=env.action_space.shape[0],
            proprio_dim=env.observation_space["proprioception"].shape[0],
            goal_dim=env.observation_space["goal"].shape[0],
            vision_encoder=args.vision_encoder,
            hidden_dim=args.hidden_dim,
        )
    else:
        policy = RNNPolicy(
            action_dim=env.action_space.shape[0],
            proprio_dim=env.observation_space["proprioception"].shape[0],
            goal_dim=env.observation_space["goal"].shape[0],
            vision_encoder=args.vision_encoder,
            hidden_dim=args.hidden_dim,
        )
    
    # Load checkpoint
    checkpoint = torch.load(args.checkpoint, map_location=device)
    if "policy_state_dict" in checkpoint:
        policy.load_state_dict(checkpoint["policy_state_dict"])
    else:
        policy.load_state_dict(checkpoint)
    
    policy = policy.to(device)
    policy.eval()
    
    # Evaluation metrics
    metrics = {
        "success_rate": 0.0,
        "avg_steps": 0.0,
        "avg_reward": 0.0,
        "episodes": [],
    }
    
    # Run evaluation episodes
    for ep in tqdm(range(args.episodes), desc="Evaluating"):
        obs, _ = env.reset(seed=args.seed + ep)
        done = False
        
        ep_reward = 0.0
        ep_steps = 0
        frames = []
        
        # Initialize hidden state for RNN
        if args.policy_type == "rnn":
            hidden = policy.init_hidden(1, device)
        
        while not done and ep_steps < args.max_steps:
            # Prepare observation
            obs_tensor = {
                k: torch.from_numpy(v).unsqueeze(0).to(device)
                for k, v in obs.items()
            }
            
            # Get action
            with torch.no_grad():
                if args.policy_type == "mlp":
                    action = policy.get_action(obs_tensor, deterministic=True)
                else:
                    action, hidden = policy.get_action(obs_tensor, hidden, deterministic=True)
            
            action = action.cpu().numpy()[0]
            
            # Step environment
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            ep_reward += reward
            ep_steps += 1
            
            # Render
            if args.render:
                frame = env.render()
                if frame is not None:
                    frames.append(frame)
        
        # Record metrics
        success = info.get("success", False)
        metrics["success_rate"] += float(success)
        metrics["avg_steps"] += ep_steps
        metrics["avg_reward"] += ep_reward
        
        metrics["episodes"].append({
            "episode": ep,
            "success": success,
            "steps": ep_steps,
            "reward": ep_reward,
            "distance": info.get("distance", 0.0),
        })
        
        # Save video
        if args.render and len(frames) > 0:
            os.makedirs("videos", exist_ok=True)
            video_path = f"videos/{args.task}_ep{ep}.mp4"
            imageio.mimsave(video_path, frames, fps=30)
            print(f"Saved video to {video_path}")
    
    # Compute averages
    metrics["success_rate"] /= args.episodes
    metrics["avg_steps"] /= args.episodes
    metrics["avg_reward"] /= args.episodes
    
    # Print results
    print("\n" + "="*50)
    print(f"Evaluation Results ({args.episodes} episodes)")
    print("="*50)
    print(f"Success Rate: {metrics['success_rate']*100:.1f}%")
    print(f"Avg Steps: {metrics['avg_steps']:.1f}")
    print(f"Avg Reward: {metrics['avg_reward']:.2f}")
    print("="*50)
    
    # Save metrics
    os.makedirs("results", exist_ok=True)
    results_path = f"results/{args.task}_eval.json"
    with open(results_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\nSaved detailed metrics to {results_path}")
    
    env.close()
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True, choices=["pick_place", "drawer", "button"])
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to policy checkpoint")
    parser.add_argument("--policy_type", type=str, default="mlp", choices=["mlp", "rnn"])
    parser.add_argument("--vision_encoder", type=str, default="simple", choices=["simple", "vit"])
    parser.add_argument("--hidden_dim", type=int, default=256)
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--max_steps", type=int, default=500)
    parser.add_argument("--render", action="store_true", help="Render and save videos")
    parser.add_argument("--seed", type=int, default=0)
    
    args = parser.parse_args()
    evaluate_policy(args)
