"""Action mapper: converts policy output to MuJoCo actuator commands."""
import numpy as np
from typing import Optional


class ActionMapper:
    """
    Maps policy actions to MuJoCo actuator commands.
    
    Handles:
    - Action scaling and clipping
    - Coordinate frame transformations
    - Safety constraints
    - Smoothing/filtering
    """
    
    def __init__(
        self,
        action_dim: int,
        action_scale: float = 1.0,
        use_smoothing: bool = False,
        smoothing_alpha: float = 0.3,
    ):
        self.action_dim = action_dim
        self.action_scale = action_scale
        self.use_smoothing = use_smoothing
        self.smoothing_alpha = smoothing_alpha
        
        self.prev_action = None
    
    def map(self, policy_action: np.ndarray) -> np.ndarray:
        """
        Map policy action to actuator commands.
        
        Args:
            policy_action: (action_dim,) array in [-1, 1]
        
        Returns:
            actuator_cmd: (action_dim,) array
        """
        # Clip to valid range
        action = np.clip(policy_action, -1.0, 1.0)
        
        # Scale
        action = action * self.action_scale
        
        # Smooth with previous action
        if self.use_smoothing and self.prev_action is not None:
            action = (
                self.smoothing_alpha * action +
                (1 - self.smoothing_alpha) * self.prev_action
            )
        
        self.prev_action = action.copy()
        
        return action
    
    def reset(self):
        """Reset mapper state."""
        self.prev_action = None
    
    def apply_safety_constraints(
        self,
        action: np.ndarray,
        joint_pos: np.ndarray,
        joint_limits: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Apply safety constraints to action.
        
        Args:
            action: proposed action
            joint_pos: current joint positions
            joint_limits: (action_dim, 2) array of [min, max] limits
        
        Returns:
            safe_action: constrained action
        """
        if joint_limits is None:
            return action
        
        # Predict next joint position
        next_pos = joint_pos + action * 0.02  # Assume 50Hz control
        
        # Clip to limits with margin
        margin = 0.1
        for i in range(len(action)):
            if next_pos[i] < joint_limits[i, 0] + margin:
                action[i] = max(0, action[i])
            elif next_pos[i] > joint_limits[i, 1] - margin:
                action[i] = min(0, action[i])
        
        return action
