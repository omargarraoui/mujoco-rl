import numpy as np
import mujoco
import gymnasium as gym
from gymnasium import spaces
from typing import Dict, Tuple, Any, Optional
import cv2


class MuJoCoManipulationEnv(gym.Env):
    """Base environment for MuJoCo manipulation tasks."""
    
    metadata = {"render_modes": ["rgb_array", "human"], "render_fps": 30}
    
    def __init__(
        self,
        model_path: str,
        frame_skip: int = 5,
        render_mode: Optional[str] = None,
        camera_id: int = 0,
        image_size: Tuple[int, int] = (224, 224),
    ):
        super().__init__()
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        self.frame_skip = frame_skip
        self.render_mode = render_mode
        self.camera_id = camera_id
        self.image_size = image_size
        
        # Renderer for RGB observations
        self.renderer = mujoco.Renderer(self.model, height=image_size[0], width=image_size[1])
        
        # Action space: continuous control for robot joints
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(self.model.nu,), dtype=np.float32
        )
        
        # Observation space: RGB + proprioception
        self.observation_space = spaces.Dict({
            "image": spaces.Box(0, 255, shape=(*image_size, 3), dtype=np.uint8),
            "proprioception": spaces.Box(-np.inf, np.inf, shape=(self._get_proprio_dim(),), dtype=np.float32),
            "goal": spaces.Box(-np.inf, np.inf, shape=(self._get_goal_dim(),), dtype=np.float32),
        })
        
    def _get_proprio_dim(self) -> int:
        """Get proprioception dimension (joint positions + velocities)."""
        return self.model.nq + self.model.nv
    
    def _get_goal_dim(self) -> int:
        """Get goal dimension (task-specific, override in subclasses)."""
        return 3  # Default: 3D target position
    
    def _get_obs(self) -> Dict[str, np.ndarray]:
        """Get current observation."""
        # Render RGB image
        self.renderer.update_scene(self.data, camera=self.camera_id)
        image = self.renderer.render()
        
        # Get proprioception
        qpos = self.data.qpos.copy()
        qvel = self.data.qvel.copy()
        proprio = np.concatenate([qpos, qvel])
        
        # Get goal (task-specific)
        goal = self._get_goal()
        
        return {
            "image": image,
            "proprioception": proprio.astype(np.float32),
            "goal": goal.astype(np.float32),
        }
    
    def _get_goal(self) -> np.ndarray:
        """Get current goal (override in subclasses)."""
        return np.zeros(self._get_goal_dim(), dtype=np.float32)
    
    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        """Reset environment."""
        super().reset(seed=seed)
        
        mujoco.mj_resetData(self.model, self.data)
        self._reset_task()
        
        obs = self._get_obs()
        info = {}
        
        return obs, info
    
    def _reset_task(self):
        """Reset task-specific state (override in subclasses)."""
        pass
    
    def step(self, action: np.ndarray) -> Tuple[Dict, float, bool, bool, Dict]:
        """Execute action and return transition."""
        # Clip and apply action
        action = np.clip(action, -1.0, 1.0)
        self.data.ctrl[:] = action
        
        # Step simulation
        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)
        
        # Get observation
        obs = self._get_obs()
        
        # Compute reward and check termination
        reward = self._compute_reward()
        terminated = bool(self._check_terminated())
        truncated = bool(self._check_truncated())
        info = self._get_info()
        
        return obs, reward, terminated, truncated, info
    
    def _compute_reward(self) -> float:
        """Compute reward (override in subclasses)."""
        return 0.0
    
    def _check_terminated(self) -> bool:
        """Check if episode is terminated (override in subclasses)."""
        return False
    
    def _check_truncated(self) -> bool:
        """Check if episode is truncated (override in subclasses)."""
        return self.data.time > 10.0  # Default 10s timeout
    
    def _get_info(self) -> Dict[str, Any]:
        """Get info dict (override in subclasses)."""
        return {"success": False}
    
    def render(self):
        """Render environment."""
        if self.render_mode == "rgb_array":
            self.renderer.update_scene(self.data, camera=self.camera_id)
            return self.renderer.render()
        return None
    
    def close(self):
        """Clean up resources."""
        if hasattr(self, 'renderer'):
            self.renderer.close()
