"""Reinforcement learning training script using Stable-Baselines3."""
import argparse
import torch
import numpy as np
from stable_baselines3 import PPO, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
import os

from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv
from train.wrappers import FlattenObsWrapper


def make_env(task: str, rank: int, seed: int = 0):
    """Create environment factory."""
    def _init():
        if task == "pick_place":
            env = PickPlaceEnv(render_mode=None)
        elif task == "drawer":
            env = DrawerEnv(task_mode="open", render_mode=None)
        elif task == "button":
            env = ToolUseEnv(tool_type="button", render_mode=None)
        else:
            raise ValueError(f"Unknown task: {task}")
        
        env = FlattenObsWrapper(env)
        env = Monitor(env)
        env.reset(seed=seed + rank)
        return env
    return _init


def train_rl(args):
    """Train policy with RL."""
    # Create vectorized environments
    if args.num_envs > 1:
        env = SubprocVecEnv([make_env(args.task, i, args.seed) for i in range(args.num_envs)])
    else:
        env = DummyVecEnv([make_env(args.task, 0, args.seed)])
    
    # Create eval environment
    eval_env = DummyVecEnv([make_env(args.task, 0, args.seed + 1000)])
    
    # Create algorithm
    if args.algo == "ppo":
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=args.lr,
            n_steps=args.n_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=args.gamma,
            verbose=1,
            tensorboard_log=f"runs/rl_{args.task}",
        )
    elif args.algo == "sac":
        model = SAC(
            "MlpPolicy",
            env,
            learning_rate=args.lr,
            buffer_size=args.buffer_size,
            batch_size=args.batch_size,
            gamma=args.gamma,
            verbose=1,
            tensorboard_log=f"runs/rl_{args.task}",
        )
    else:
        raise ValueError(f"Unknown algorithm: {args.algo}")
    
    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=args.save_freq,
        save_path=f"checkpoints/rl_{args.task}_{args.algo}",
        name_prefix="model",
    )
    
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"checkpoints/rl_{args.task}_{args.algo}",
        log_path=f"logs/rl_{args.task}_{args.algo}",
        eval_freq=args.eval_freq,
        n_eval_episodes=10,
        deterministic=True,
    )
    
    # Train
    model.learn(
        total_timesteps=args.total_timesteps,
        callback=[checkpoint_callback, eval_callback],
    )
    
    # Save final model
    os.makedirs("checkpoints", exist_ok=True)
    model.save(f"checkpoints/rl_{args.task}_{args.algo}_final")
    print(f"Training complete. Model saved to checkpoints/rl_{args.task}_{args.algo}_final")
    
    env.close()
    eval_env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="pick_place", choices=["pick_place", "drawer", "button"])
    parser.add_argument("--algo", type=str, default="ppo", choices=["ppo", "sac"])
    parser.add_argument("--num_envs", type=int, default=4)
    parser.add_argument("--total_timesteps", type=int, default=1000000)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--n_steps", type=int, default=2048)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--n_epochs", type=int, default=10)
    parser.add_argument("--buffer_size", type=int, default=100000)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--save_freq", type=int, default=10000)
    parser.add_argument("--eval_freq", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    
    args = parser.parse_args()
    train_rl(args)
