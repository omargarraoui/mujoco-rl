import torch
import torch.nn as nn
from typing import Dict, Optional, Tuple
from perception.vision_encoder import VisionEncoder, SimpleConvEncoder


class RNNPolicy(nn.Module):
    """RNN policy for temporal reasoning."""
    
    def __init__(
        self,
        action_dim: int,
        proprio_dim: int,
        goal_dim: int,
        vision_encoder: str = "simple",
        hidden_dim: int = 256,
        num_layers: int = 2,
        rnn_type: str = "gru",  # "gru" or "lstm"
    ):
        super().__init__()
        
        # Vision encoder
        if vision_encoder == "vit":
            self.vision_encoder = VisionEncoder(embedding_dim=hidden_dim)
        else:
            self.vision_encoder = SimpleConvEncoder(embedding_dim=hidden_dim)
        
        # Input dimension
        input_dim = hidden_dim + proprio_dim + goal_dim
        
        # RNN
        if rnn_type == "lstm":
            self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        else:
            self.rnn = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True)
        
        # Action head
        self.action_head = nn.Linear(hidden_dim, action_dim)
        
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.rnn_type = rnn_type
    
    def forward(
        self,
        obs: Dict[str, torch.Tensor],
        hidden: Optional[Tuple[torch.Tensor, ...]] = None,
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, ...]]:
        """
        Compute action from observation with RNN state.
        
        Args:
            obs: dict with keys "image", "proprioception", "goal"
            hidden: RNN hidden state (optional)
        
        Returns:
            action: (B, action_dim) tensor
            hidden: updated RNN hidden state
        """
        batch_size = obs["image"].shape[0]
        
        # Encode image - convert from (B, H, W, C) to (B, C, H, W)
        image = obs["image"].float() / 255.0
        if image.dim() == 4 and image.shape[-1] == 3:
            image = image.permute(0, 3, 1, 2)  # (B, H, W, C) -> (B, C, H, W)
        vision_emb = self.vision_encoder(image)
        
        # Concatenate inputs
        proprio = obs["proprioception"]
        goal = obs["goal"]
        x = torch.cat([vision_emb, proprio, goal], dim=-1)
        
        # Add sequence dimension
        x = x.unsqueeze(1)  # (B, 1, input_dim)
        
        # RNN forward
        if hidden is None:
            rnn_out, hidden = self.rnn(x)
        else:
            rnn_out, hidden = self.rnn(x, hidden)
        
        # Remove sequence dimension
        rnn_out = rnn_out.squeeze(1)  # (B, hidden_dim)
        
        # Action output
        action = torch.tanh(self.action_head(rnn_out))
        
        return action, hidden
    
    def get_action(
        self,
        obs: Dict[str, torch.Tensor],
        hidden: Optional[Tuple[torch.Tensor, ...]] = None,
        deterministic: bool = True,
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, ...]]:
        """Get action with hidden state."""
        return self.forward(obs, hidden)
    
    def init_hidden(self, batch_size: int, device: torch.device) -> Tuple[torch.Tensor, ...]:
        """Initialize hidden state."""
        if self.rnn_type == "lstm":
            h = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
            c = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
            return (h, c)
        else:
            h = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
            return h  # Return tensor directly for GRU, not tuple
