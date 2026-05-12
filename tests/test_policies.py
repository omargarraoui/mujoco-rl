"""Unit tests for policies."""
import pytest
import torch
import numpy as np
from policies.mlp_policy import MLPPolicy
from policies.rnn_policy import RNNPolicy


def test_mlp_policy():
    """Test MLP policy."""
    policy = MLPPolicy(
        action_dim=3,
        proprio_dim=12,
        goal_dim=3,
        vision_encoder="simple",
        hidden_dim=128,
    )
    
    # Test forward pass
    obs = {
        "image": torch.randint(0, 255, (2, 224, 224, 3), dtype=torch.uint8),
        "proprioception": torch.randn(2, 12),
        "goal": torch.randn(2, 3),
    }
    
    action = policy(obs)
    assert action.shape == (2, 3)
    assert torch.all(action >= -1.0) and torch.all(action <= 1.0)


def test_rnn_policy():
    """Test RNN policy."""
    policy = RNNPolicy(
        action_dim=3,
        proprio_dim=12,
        goal_dim=3,
        vision_encoder="simple",
        hidden_dim=128,
        num_layers=2,
    )
    
    # Test forward pass
    obs = {
        "image": torch.randint(0, 255, (2, 224, 224, 3), dtype=torch.uint8),
        "proprioception": torch.randn(2, 12),
        "goal": torch.randn(2, 3),
    }
    
    hidden = policy.init_hidden(2, torch.device("cpu"))
    action, new_hidden = policy(obs, hidden)
    
    assert action.shape == (2, 3)
    assert torch.all(action >= -1.0) and torch.all(action <= 1.0)
    assert len(new_hidden) > 0


def test_policy_determinism():
    """Test that policy is deterministic with same input."""
    policy = MLPPolicy(
        action_dim=3,
        proprio_dim=12,
        goal_dim=3,
        vision_encoder="simple",
        hidden_dim=128,
    )
    policy.eval()
    
    obs = {
        "image": torch.randint(0, 255, (1, 224, 224, 3), dtype=torch.uint8),
        "proprioception": torch.randn(1, 12),
        "goal": torch.randn(1, 3),
    }
    
    with torch.no_grad():
        action1 = policy(obs)
        action2 = policy(obs)
    
    torch.testing.assert_close(action1, action2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
