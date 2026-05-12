import numpy as np
from envs.base_env import MuJoCoManipulationEnv
from typing import Optional, Dict


class PickPlaceEnv(MuJoCoManipulationEnv):
    """Pick and place task environment."""
    
    def __init__(self, **kwargs):
        # Use simple reach XML for now (can be replaced with actual pick-place scene)
        model_path = kwargs.pop("model_path", "envs/assets/pick_place.xml")
        super().__init__(model_path, **kwargs)
        
        self.target_pos = np.zeros(3)
        self.object_pos = np.zeros(3)
        self.success_threshold = 0.05  # 5cm
        
    def _get_goal_dim(self) -> int:
        return 3  # Target 3D position
    
    def _get_goal(self) -> np.ndarray:
        return self.target_pos.copy()
    
    def _reset_task(self):
        """Randomize object and target positions."""
        # Randomize object position on table
        self.object_pos = np.array([
            self.np_random.uniform(0.3, 0.5),
            self.np_random.uniform(-0.2, 0.2),
            0.02  # On table surface
        ])
        
        # Randomize target position
        self.target_pos = np.array([
            self.np_random.uniform(0.3, 0.5),
            self.np_random.uniform(-0.2, 0.2),
            0.15  # Above table
        ])
        
        # Set object position in simulation (if object body exists)
        if self.model.nbody > 1:
            obj_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "object")
            if obj_id >= 0:
                self.data.qpos[-7:-4] = self.object_pos
    
    def _compute_reward(self) -> float:
        """Dense reward based on object-to-target distance."""
        # Get current object position
        if self.model.nbody > 1:
            obj_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "object")
            if obj_id >= 0:
                obj_pos = self.data.xpos[obj_id]
            else:
                obj_pos = self.object_pos
        else:
            # Fallback: use end-effector position
            obj_pos = self.data.site_xpos[0] if self.model.nsite > 0 else np.zeros(3)
        
        # Distance to target
        dist = np.linalg.norm(obj_pos - self.target_pos)
        reward = -dist
        
        # Bonus for success
        if dist < self.success_threshold:
            reward += 10.0
        
        return reward
    
    def _check_terminated(self) -> bool:
        """Terminate on success."""
        if self.model.nbody > 1:
            obj_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "object")
            if obj_id >= 0:
                obj_pos = self.data.xpos[obj_id]
            else:
                return False
        else:
            obj_pos = self.data.site_xpos[0] if self.model.nsite > 0 else np.zeros(3)
        
        dist = np.linalg.norm(obj_pos - self.target_pos)
        return dist < self.success_threshold
    
    def _get_info(self) -> Dict:
        """Return success info."""
        if self.model.nbody > 1:
            obj_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "object")
            if obj_id >= 0:
                obj_pos = self.data.xpos[obj_id]
            else:
                obj_pos = np.zeros(3)
        else:
            obj_pos = self.data.site_xpos[0] if self.model.nsite > 0 else np.zeros(3)
        
        dist = np.linalg.norm(obj_pos - self.target_pos)
        return {
            "success": dist < self.success_threshold,
            "distance": dist,
        }


import mujoco
