"""Demo script: visualize single rollout with trained policy."""
import argparse
import torch
import numpy as np
import imageio

from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv
from policies.mlp_policy import MLPPolicy
from policies.rnn_policy import RNNPolicy


def run_demo(args):
    """Run single demo rollout."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create environment
    if args.task == "pick_place":
        env = PickPlaceEnv(render_mode="rgb_array")
    elif args.task == "drawer":
        env = DrawerEnv(task_mode="open", render_mode="rgb_array")
    elif args.task == "button":
        env = ToolUseEnv(tool_type="button", render_mode="rgb_array")
    else:
        raise ValueError(f"Unknown task: {args.task}")
    
    # Load policy if checkpoint provided
    if args.checkpoint:
        if args.policy_type == "mlp":
            policy = MLPPolicy(
                action_dim=env.action_space.shape[0],
                proprio_dim=env.observation_space["proprioception"].shape[0],
                goal_dim=env.observation_space["goal"].shape[0],
                vision_encoder=args.vision_encoder,
            )
        else:
            policy = RNNPolicy(
                action_dim=env.action_space.shape[0],
                proprio_dim=env.observation_space["proprioception"].shape[0],
                goal_dim=env.observation_space["goal"].shape[0],
                vision_encoder=args.vision_encoder,
            )
        
        checkpoint = torch.load(args.checkpoint, map_location=device)
        if "policy_state_dict" in checkpoint:
            policy.load_state_dict(checkpoint["policy_state_dict"])
        else:
            policy.load_state_dict(checkpoint)
        
        policy = policy.to(device)
        policy.eval()
        print(f"Loaded policy from {args.checkpoint}")
    else:
        policy = None
        print("Running with random policy")
    
    # Run episode
    obs, _ = env.reset(seed=args.seed)
    done = False
    frames = []
    
    if policy and args.policy_type == "rnn":
        hidden = policy.init_hidden(1, device)
    
    step = 0
    while not done and step < args.max_steps:
        # Get action
        if policy:
            obs_tensor = {
                k: torch.from_numpy(v).unsqueeze(0).to(device)
                for k, v in obs.items()
            }
            with torch.no_grad():
                if args.policy_type == "mlp":
                    action = policy.get_action(obs_tensor, deterministic=True)
                else:
                    action, hidden = policy.get_action(obs_tensor, hidden, deterministic=True)
            action = action.cpu().numpy()[0]
        else:
            action = env.action_space.sample()
        
        # Step
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # Render
        frame = env.render()
        if frame is not None:
            frames.append(frame)
        
        step += 1
    
    print(f"Episode finished: steps={step}, success={info.get('success', False)}")
    
    # Save video
    if len(frames) > 0:
        video_path = f"demo_{args.task}.mp4"
        imageio.mimsave(video_path, frames, fps=30)
        print(f"Saved video to {video_path}")
    
    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True, choices=["pick_place", "drawer", "button"])
    parser.add_argument("--checkpoint", type=str, default=None, help="Path to policy checkpoint (optional)")
    parser.add_argument("--policy_type", type=str, default="mlp", choices=["mlp", "rnn"])
    parser.add_argument("--vision_encoder", type=str, default="simple", choices=["simple", "vit"])
    parser.add_argument("--max_steps", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    
    args = parser.parse_args()
    run_demo(args)
