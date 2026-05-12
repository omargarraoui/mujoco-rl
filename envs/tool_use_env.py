import numpy as np
import mujoco
from envs.base_env import MuJoCoManipulationEnv
from typing import Dict


class ToolUseEnv(MuJoCoManipulationEnv):
    """Tool use task (button press, lever, stick)."""
    
    def __init__(self, tool_type="button", **kwargs):
        model_path = kwargs.pop("model_path", f"envs/assets/{tool_type}.xml")
        super().__init__(model_path, **kwargs)
        
        self.tool_type = tool_type  # "button", "lever", "stick"
        self.target_state = 1.0  # Activated state
        self.success_threshold = 0.1
        
    def _get_goal_dim(self) -> int:
        return 1  # Tool activation state
    
    def _get_goal(self) -> np.ndarray:
        return np.array([self.target_state], dtype=np.float32)
    
    def _reset_task(self):
        """Reset tool to inactive state."""
        # Tool starts in default position
        pass
    
    def _get_tool_state(self) -> float:
        """Get current tool activation state."""
        if self.tool_type == "button":
            # Check button press depth
            if self.model.nsensor > 0:
                return self.data.sensordata[0]
        elif self.tool_type == "lever":
            # Check lever angle
            if self.model.njnt > 0:
                return self.data.qpos[-1]
        elif self.tool_type == "stick":
            # Check stick contact with target
            if self.model.nsensor > 0:
                return float(self.data.sensordata[0] > 0.1)
        return 0.0
    
    def _compute_reward(self) -> float:
        """Reward based on tool activation."""
        current_state = self._get_tool_state()
        dist = abs(current_state - self.target_state)
        reward = -dist * 5.0
        
        # Success bonus
        if dist < self.success_threshold:
            reward += 10.0
        
        return reward
    
    def _check_terminated(self) -> bool:
        """Terminate on success."""
        current_state = self._get_tool_state()
        dist = abs(current_state - self.target_state)
        return dist < self.success_threshold
    
    def _get_info(self) -> Dict:
        """Return success info."""
        current_state = self._get_tool_state()
        dist = abs(current_state - self.target_state)
        return {
            "success": dist < self.success_threshold,
            "tool_state": current_state,
            "distance": dist,
        }
