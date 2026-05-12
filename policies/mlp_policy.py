import torch
import torch.nn as nn
from typing import Dict, Tuple
from perception.vision_encoder import VisionEncoder, SimpleConvEncoder


class MLPPolicy(nn.Module):
    """MLP policy with vision encoder."""
    
    def __init__(
        self,
        action_dim: int,
        proprio_dim: int,
        goal_dim: int,
        vision_encoder: str = "simple",  # "simple" or "vit"
        hidden_dim: int = 256,
        num_layers: int = 3,
    ):
        super().__init__()
        
        # Vision encoder
        if vision_encoder == "vit":
            self.vision_encoder = VisionEncoder(embedding_dim=hidden_dim)
        else:
            self.vision_encoder = SimpleConvEncoder(embedding_dim=hidden_dim)
        
        # Input dimension: vision + proprio + goal
        input_dim = hidden_dim + proprio_dim + goal_dim
        
        # MLP layers
        layers = []
        for i in range(num_layers):
            if i == 0:
                layers.extend([
                    nn.Linear(input_dim, hidden_dim),
                    nn.ReLU(),
                ])
            else:
                layers.extend([
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                ])
        
        self.mlp = nn.Sequential(*layers)
        
        # Action head
        self.action_head = nn.Linear(hidden_dim, action_dim)
        
        self.action_dim = action_dim
    
    def forward(self, obs: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Compute action from observation.
        
        Args:
            obs: dict with keys "image", "proprioception", "goal"
        
        Returns:
            action: (B, action_dim) tensor in [-1, 1]
        """
        # Encode image - convert from (B, H, W, C) to (B, C, H, W)
        image = obs["image"].float() / 255.0  # Normalize to [0, 1]
        if image.dim() == 4 and image.shape[-1] == 3:
            image = image.permute(0, 3, 1, 2)  # (B, H, W, C) -> (B, C, H, W)
        vision_emb = self.vision_encoder(image)
        
        # Concatenate all inputs
        proprio = obs["proprioception"]
        goal = obs["goal"]
        x = torch.cat([vision_emb, proprio, goal], dim=-1)
        
        # MLP forward
        x = self.mlp(x)
        
        # Action output
        action = torch.tanh(self.action_head(x))
        
        return action
    
    def get_action(self, obs: Dict[str, torch.Tensor], deterministic: bool = True) -> torch.Tensor:
        """Get action (for compatibility with RL algorithms)."""
        return self.forward(obs)
