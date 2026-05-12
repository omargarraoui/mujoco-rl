# API Reference

## Environments

### `MuJoCoManipulationEnv`

Base class for all manipulation environments.

```python
from envs import MuJoCoManipulationEnv

env = MuJoCoManipulationEnv(
    model_path="path/to/scene.xml",
    frame_skip=5,
    render_mode="rgb_array",
    camera_id=0,
    image_size=(224, 224),
)
```

**Methods**:
- `reset(seed=None, options=None) -> (obs, info)`
- `step(action) -> (obs, reward, terminated, truncated, info)`
- `render() -> np.ndarray`
- `close()`

**Observation Space**:
```python
{
    "image": Box(0, 255, (224, 224, 3), uint8),
    "proprioception": Box(-inf, inf, (n_joints*2,), float32),
    "goal": Box(-inf, inf, (goal_dim,), float32),
}
```

**Action Space**:
```python
Box(-1.0, 1.0, (n_actuators,), float32)
```

### `PickPlaceEnv`

Pick and place task.

```python
from envs import PickPlaceEnv

env = PickPlaceEnv(render_mode="rgb_array")
obs, info = env.reset()
```

**Goal**: 3D target position for object placement.

### `DrawerEnv`

Drawer manipulation task.

```python
from envs import DrawerEnv

env = DrawerEnv(task_mode="open")  # or "close"
```

**Goal**: Target drawer opening amount (0.0 to 0.3).

### `ToolUseEnv`

Tool use task (button, lever, stick).

```python
from envs import ToolUseEnv

env = ToolUseEnv(tool_type="button")  # or "lever", "stick"
```

**Goal**: Tool activation state.

## Policies

### `MLPPolicy`

Feedforward policy network.

```python
from policies import MLPPolicy

policy = MLPPolicy(
    action_dim=3,
    proprio_dim=12,
    goal_dim=3,
    vision_encoder="simple",  # or "vit"
    hidden_dim=256,
    num_layers=3,
)

action = policy(obs)  # obs is dict with image, proprioception, goal
```

### `RNNPolicy`

Recurrent policy network.

```python
from policies import RNNPolicy

policy = RNNPolicy(
    action_dim=3,
    proprio_dim=12,
    goal_dim=3,
    vision_encoder="simple",
    hidden_dim=256,
    num_layers=2,
    rnn_type="gru",  # or "lstm"
)

hidden = policy.init_hidden(batch_size=1, device=device)
action, hidden = policy(obs, hidden)
```

## Perception

### `VisionEncoder`

ViT-based vision encoder.

```python
from perception import VisionEncoder

encoder = VisionEncoder(
    model_name="vit_small_patch16_224",
    pretrained=True,
    embedding_dim=256,
    freeze_backbone=False,
)

# Input: (B, 3, 224, 224) in [0, 1]
# Output: (B, 256)
embedding = encoder(image)
```

### `SimpleConvEncoder`

Lightweight CNN encoder.

```python
from perception import SimpleConvEncoder

encoder = SimpleConvEncoder(embedding_dim=256)
embedding = encoder(image)
```

## Planner

### `HierarchicalPlanner`

Goal decomposition planner.

```python
from planner import HierarchicalPlanner

planner = HierarchicalPlanner(task="pick_place")
subgoals = planner.plan(obs, goal)
current_subgoal = planner.get_current_subgoal()
planner.advance_subgoal()
```

## Controllers

### `ActionMapper`

Maps policy actions to actuator commands.

```python
from controllers import ActionMapper

mapper = ActionMapper(
    action_dim=3,
    action_scale=1.0,
    use_smoothing=True,
    smoothing_alpha=0.3,
)

actuator_cmd = mapper.map(policy_action)
mapper.reset()
```

## Training

### Behavior Cloning

```python
from train.train_bc import train_bc

args = argparse.Namespace(
    task="pick_place",
    policy_type="mlp",
    vision_encoder="simple",
    action_dim=3,
    proprio_dim=12,
    goal_dim=3,
    hidden_dim=256,
    data_path="data/expert.pt",
    num_expert_episodes=100,
    epochs=50,
    batch_size=64,
    lr=3e-4,
    save_freq=10,
)

train_bc(args)
```

### Reinforcement Learning

```python
from train.train_rl import train_rl

args = argparse.Namespace(
    task="pick_place",
    algo="ppo",
    num_envs=4,
    total_timesteps=1000000,
    lr=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    save_freq=10000,
    eval_freq=5000,
    seed=0,
)

train_rl(args)
```

## Evaluation

```python
from eval import evaluate_policy

args = argparse.Namespace(
    task="pick_place",
    checkpoint="checkpoints/model.pt",
    policy_type="mlp",
    vision_encoder="simple",
    hidden_dim=256,
    episodes=50,
    max_steps=500,
    render=True,
    seed=0,
)

metrics = evaluate_policy(args)
# Returns: {"success_rate": 0.8, "avg_steps": 120, "avg_reward": 5.2, ...}
```

## Utilities

### Video Saving

```python
from utils.video import save_video

frames = [...]  # List of (H, W, 3) RGB frames
save_video(frames, "output.mp4", fps=30)
```

### Logging

```python
from utils.logging import setup_logger

logger = setup_logger("my_experiment", log_file="logs/exp.log")
logger.info("Training started")
```

## Custom Extensions

### Adding a New Environment

```python
from envs.base_env import MuJoCoManipulationEnv

class MyTaskEnv(MuJoCoManipulationEnv):
    def __init__(self, **kwargs):
        super().__init__(model_path="envs/assets/my_task.xml", **kwargs)
    
    def _get_goal_dim(self) -> int:
        return 3  # Goal dimension
    
    def _reset_task(self):
        # Initialize task-specific state
        pass
    
    def _compute_reward(self) -> float:
        # Compute reward
        return 0.0
    
    def _check_terminated(self) -> bool:
        # Check success condition
        return False
    
    def _get_info(self) -> dict:
        return {"success": False}
```

### Adding a New Policy

```python
import torch.nn as nn

class MyPolicy(nn.Module):
    def __init__(self, action_dim, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Tanh(),
        )
    
    def forward(self, obs):
        return self.net(obs)
```
