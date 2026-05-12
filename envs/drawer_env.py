import numpy as np
import mujoco
from envs.base_env import MuJoCoManipulationEnv
from typing import Dict


class DrawerEnv(MuJoCoManipulationEnv):
    """Drawer open/close task environment."""
    
    def __init__(self, task_mode="open", **kwargs):
        model_path = kwargs.pop("model_path", "envs/assets/drawer.xml")
        super().__init__(model_path, **kwargs)
        
        self.task_mode = task_mode  # "open" or "close"
        self.target_opening = 0.3 if task_mode == "open" else 0.0
        self.success_threshold = 0.05
        
    def _get_goal_dim(self) -> int:
        return 1  # Drawer opening amount
    
    def _get_goal(self) -> np.ndarray:
        return np.array([self.target_opening], dtype=np.float32)
    
    def _reset_task(self):
        """Reset drawer to initial state."""
        # Set drawer to closed (open) position based on task
        if self.task_mode == "open":
            initial_opening = 0.0
        else:
            initial_opening = 0.3
        
        # Set drawer joint position (assumes last joint is drawer slide)
        if self.model.njnt > 0:
            self.data.qpos[-1] = initial_opening
    
    def _get_drawer_opening(self) -> float:
        """Get current drawer opening amount."""
        if self.model.njnt > 0:
            return self.data.qpos[-1]
        return 0.0
    
    def _compute_reward(self) -> float:
        """Reward based on drawer opening progress."""
        current_opening = self._get_drawer_opening()
        dist = abs(current_opening - self.target_opening)
        reward = -dist * 10.0
        
        # Success bonus
        if dist < self.success_threshold:
            reward += 10.0
        
        return reward
    
    def _check_terminated(self) -> bool:
        """Terminate on success."""
        current_opening = self._get_drawer_opening()
        dist = abs(current_opening - self.target_opening)
        return dist < self.success_threshold
    
    def _get_info(self) -> Dict:
        """Return success info."""
        current_opening = self._get_drawer_opening()
        dist = abs(current_opening - self.target_opening)
        return {
            "success": dist < self.success_threshold,
            "opening": current_opening,
            "distance": dist,
        }
