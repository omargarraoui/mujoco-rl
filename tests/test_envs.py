"""Unit tests for environments."""
import pytest
import numpy as np
from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv


def test_pick_place_env():
    """Test pick and place environment."""
    env = PickPlaceEnv(render_mode=None)
    
    # Test reset
    obs, info = env.reset(seed=0)
    assert "image" in obs
    assert "proprioception" in obs
    assert "goal" in obs
    assert obs["image"].shape == (224, 224, 3)
    
    # Test step
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert "success" in info
    
    env.close()


def test_drawer_env():
    """Test drawer environment."""
    env = DrawerEnv(task_mode="open", render_mode=None)
    
    # Test reset
    obs, info = env.reset(seed=0)
    assert "image" in obs
    assert "proprioception" in obs
    assert "goal" in obs
    
    # Test step
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    assert isinstance(reward, float)
    assert "success" in info
    assert "opening" in info
    
    env.close()


def test_tool_use_env():
    """Test tool use environment."""
    env = ToolUseEnv(tool_type="button", render_mode=None)
    
    # Test reset
    obs, info = env.reset(seed=0)
    assert "image" in obs
    
    # Test step
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    assert isinstance(reward, float)
    assert "success" in info
    
    env.close()


def test_deterministic_reset():
    """Test that reset with same seed gives same initial state."""
    env = PickPlaceEnv(render_mode=None)
    
    obs1, _ = env.reset(seed=42)
    obs2, _ = env.reset(seed=42)
    
    np.testing.assert_array_equal(obs1["proprioception"], obs2["proprioception"])
    
    env.close()


def test_action_clipping():
    """Test that actions are properly clipped."""
    env = PickPlaceEnv(render_mode=None)
    env.reset(seed=0)
    
    # Test extreme actions
    action = np.array([10.0, -10.0, 5.0])
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Should not crash
    assert obs is not None
    
    env.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
