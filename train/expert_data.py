"""Generate expert demonstrations using scripted policy."""
import numpy as np
import torch
from tqdm import tqdm
import os

from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv


def scripted_pick_place_policy(obs, env):
    """Simple scripted policy for pick and place."""
    # Get end-effector position (approximate from joint angles)
    qpos = obs["proprioception"][:3]
    target = obs["goal"]
    
    # Simple proportional controller
    # This is a placeholder - real implementation would use IK
    error = np.random.randn(3) * 0.1  # Random exploration
    action = np.clip(error, -1, 1)
    
    return action


def scripted_drawer_policy(obs, env):
    """Simple scripted policy for drawer."""
    # Random exploration policy
    action = np.random.randn(3) * 0.3
    return np.clip(action, -1, 1)


def scripted_button_policy(obs, env):
    """Simple scripted policy for button press."""
    # Random exploration policy
    action = np.random.randn(3) * 0.3
    return np.clip(action, -1, 1)


def collect_expert_data(task: str, num_episodes: int, save_path: str):
    """Collect expert demonstrations."""
    # Create environment
    if task == "pick_place":
        env = PickPlaceEnv(render_mode=None)
        policy_fn = scripted_pick_place_policy
    elif task == "drawer":
        env = DrawerEnv(task_mode="open", render_mode=None)
        policy_fn = scripted_drawer_policy
    elif task == "button":
        env = ToolUseEnv(tool_type="button", render_mode=None)
        policy_fn = scripted_button_policy
    else:
        raise ValueError(f"Unknown task: {task}")
    
    # Collect data
    all_observations = {
        "image": [],
        "proprioception": [],
        "goal": [],
    }
    all_actions = []
    
    success_count = 0
    
    for ep in tqdm(range(num_episodes), desc="Collecting expert data"):
        obs, _ = env.reset(seed=ep)
        done = False
        
        ep_obs = {k: [] for k in obs.keys()}
        ep_actions = []
        
        while not done:
            # Get action from scripted policy
            action = policy_fn(obs, env)
            
            # Store transition
            for k, v in obs.items():
                ep_obs[k].append(v)
            ep_actions.append(action)
            
            # Step environment
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        
        # Only keep successful episodes (or all if success rate is low)
        if info.get("success", False) or success_count < num_episodes * 0.1:
            for k in all_observations.keys():
                all_observations[k].extend(ep_obs[k])
            all_actions.extend(ep_actions)
            
            if info.get("success", False):
                success_count += 1
    
    print(f"Collected {len(all_actions)} transitions from {num_episodes} episodes")
    print(f"Success rate: {success_count / num_episodes * 100:.1f}%")
    
    # Convert to tensors
    data = {
        "observations": {
            k: torch.from_numpy(np.array(v)) for k, v in all_observations.items()
        },
        "actions": torch.from_numpy(np.array(all_actions, dtype=np.float32)),
    }
    
    # Save
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    torch.save(data, save_path)
    print(f"Saved expert data to {save_path}")
    
    env.close()
