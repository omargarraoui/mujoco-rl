"""Gym wrappers for training."""
import gymnasium as gym
import numpy as np
from gymnasium import spaces


class FlattenObsWrapper(gym.ObservationWrapper):
    """Flatten dict observation to vector (for SB3 compatibility)."""
    
    def __init__(self, env):
        super().__init__(env)
        
        # Compute flattened observation space
        obs_dims = []
        for key in ["image", "proprioception", "goal"]:
            space = env.observation_space[key]
            obs_dims.append(int(np.prod(space.shape)))
        
        total_dim = sum(obs_dims)
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(total_dim,),
            dtype=np.float32,
        )
    
    def observation(self, obs):
        """Flatten observation dict."""
        image = obs["image"].flatten().astype(np.float32) / 255.0
        proprio = obs["proprioception"].astype(np.float32)
        goal = obs["goal"].astype(np.float32)
        
        return np.concatenate([image, proprio, goal])


class FrameStackWrapper(gym.Wrapper):
    """Stack multiple frames for temporal information."""
    
    def __init__(self, env, num_stack=4):
        super().__init__(env)
        self.num_stack = num_stack
        self.frames = []
        
        # Update observation space
        old_space = env.observation_space
        low = np.repeat(old_space.low[np.newaxis, ...], num_stack, axis=0)
        high = np.repeat(old_space.high[np.newaxis, ...], num_stack, axis=0)
        self.observation_space = spaces.Box(
            low=low,
            high=high,
            dtype=old_space.dtype,
        )
    
    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.frames = [obs] * self.num_stack
        return self._get_obs(), info
    
    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self.frames.append(obs)
        self.frames = self.frames[-self.num_stack:]
        return self._get_obs(), reward, terminated, truncated, info
    
    def _get_obs(self):
        return np.array(self.frames)
