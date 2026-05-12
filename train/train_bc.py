"""Behavior cloning training script."""
import argparse
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import os
import json

from policies.mlp_policy import MLPPolicy
from policies.rnn_policy import RNNPolicy
from train.expert_data import collect_expert_data


class ExpertDataset(Dataset):
    """Dataset of expert demonstrations."""
    
    def __init__(self, data_path: str):
        self.data = torch.load(data_path)
        self.observations = self.data["observations"]
        self.actions = self.data["actions"]
    
    def __len__(self):
        return len(self.actions)
    
    def __getitem__(self, idx):
        obs = {k: v[idx] for k, v in self.observations.items()}
        action = self.actions[idx]
        return obs, action


def train_bc(args):
    """Train policy with behavior cloning."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create policy
    if args.policy_type == "mlp":
        policy = MLPPolicy(
            action_dim=args.action_dim,
            proprio_dim=args.proprio_dim,
            goal_dim=args.goal_dim,
            vision_encoder=args.vision_encoder,
            hidden_dim=args.hidden_dim,
        )
    else:
        policy = RNNPolicy(
            action_dim=args.action_dim,
            proprio_dim=args.proprio_dim,
            goal_dim=args.goal_dim,
            vision_encoder=args.vision_encoder,
            hidden_dim=args.hidden_dim,
        )
    
    policy = policy.to(device)
    
    # Load or collect expert data
    if not os.path.exists(args.data_path):
        print(f"Collecting expert data to {args.data_path}...")
        collect_expert_data(
            task=args.task,
            num_episodes=args.num_expert_episodes,
            save_path=args.data_path,
        )
    
    # Create dataset and dataloader
    dataset = ExpertDataset(args.data_path)
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=4,
    )
    
    # Optimizer
    optimizer = torch.optim.Adam(policy.parameters(), lr=args.lr)
    criterion = nn.MSELoss()
    
    # Tensorboard
    writer = SummaryWriter(f"runs/bc_{args.task}")
    
    # Training loop
    global_step = 0
    for epoch in range(args.epochs):
        epoch_loss = 0.0
        
        for obs, actions in tqdm(dataloader, desc=f"Epoch {epoch+1}/{args.epochs}"):
            # Move to device
            obs = {k: v.to(device) for k, v in obs.items()}
            actions = actions.to(device)
            
            # Forward pass
            if args.policy_type == "mlp":
                pred_actions = policy(obs)
            else:
                pred_actions, _ = policy(obs)
            
            # Compute loss
            loss = criterion(pred_actions, actions)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Logging
            epoch_loss += loss.item()
            writer.add_scalar("train/loss", loss.item(), global_step)
            global_step += 1
        
        avg_loss = epoch_loss / len(dataloader)
        print(f"Epoch {epoch+1}: avg_loss={avg_loss:.4f}")
        
        # Save checkpoint
        if (epoch + 1) % args.save_freq == 0:
            os.makedirs("checkpoints", exist_ok=True)
            torch.save({
                "epoch": epoch,
                "policy_state_dict": policy.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            }, f"checkpoints/bc_{args.task}_epoch{epoch+1}.pt")
    
    # Save final model
    os.makedirs("checkpoints", exist_ok=True)
    torch.save(policy.state_dict(), f"checkpoints/bc_{args.task}_final.pt")
    print(f"Training complete. Model saved to checkpoints/bc_{args.task}_final.pt")
    
    writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="pick_place", choices=["pick_place", "drawer", "button"])
    parser.add_argument("--policy_type", type=str, default="mlp", choices=["mlp", "rnn"])
    parser.add_argument("--vision_encoder", type=str, default="simple", choices=["simple", "vit"])
    parser.add_argument("--action_dim", type=int, default=3)
    parser.add_argument("--proprio_dim", type=int, default=12)
    parser.add_argument("--goal_dim", type=int, default=3)
    parser.add_argument("--hidden_dim", type=int, default=256)
    parser.add_argument("--data_path", type=str, default="data/expert_pick_place.pt")
    parser.add_argument("--num_expert_episodes", type=int, default=100)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--save_freq", type=int, default=10)
    
    args = parser.parse_args()
    train_bc(args)
