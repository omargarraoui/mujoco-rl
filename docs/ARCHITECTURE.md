# Architecture

## System Overview

```
┌─────────────┐
│ Environment │ (MuJoCo simulation)
└──────┬──────┘
       │ obs (RGB + proprio + goal)
       ▼
┌─────────────┐
│ Perception  │ (Vision encoder: CNN/ViT)
└──────┬──────┘
       │ visual embedding
       ▼
┌─────────────┐
│   Planner   │ (Optional: goal decomposition)
└──────┬──────┘
       │ subgoal
       ▼
┌─────────────┐
│   Policy    │ (MLP/RNN network)
└──────┬──────┘
       │ action
       ▼
┌─────────────┐
│ Controller  │ (Action mapping + safety)
└──────┬──────┘
       │ actuator commands
       ▼
┌─────────────┐
│   MuJoCo    │
└─────────────┘
```

## Module Descriptions

### 1. Environment Layer (`envs/`)

Gym-compatible wrappers around MuJoCo scenes.

- **Base**: `MuJoCoManipulationEnv` - common interface
- **Tasks**: `PickPlaceEnv`, `DrawerEnv`, `ToolUseEnv`
- **Observations**: RGB image (224x224x3), proprioception (joint states), goal encoding
- **Actions**: continuous control (normalized to [-1, 1])

### 2. Perception Module (`perception/`)

Encodes visual observations to compact representations.

- **VisionEncoder**: ViT-based pretrained encoder
- **SimpleConvEncoder**: Lightweight CNN for fast training
- **Output**: fixed-size embedding (default 256-dim)

### 3. Policy Module (`policies/`)

Core decision-making network.

- **MLPPolicy**: feedforward network (stateless)
- **RNNPolicy**: recurrent network (GRU/LSTM) for temporal reasoning
- **Input**: vision embedding + proprioception + goal
- **Output**: continuous action vector

### 4. Planner Module (`planner/`)

Optional high-level goal decomposition.

- **HierarchicalPlanner**: decomposes tasks into subgoals
- Can be replaced with LLM/VLM-based planner
- Not required for simple tasks

### 5. Controller Module (`controllers/`)

Maps policy outputs to safe actuator commands.

- **ActionMapper**: scaling, smoothing, safety constraints
- Handles coordinate transformations
- Enforces joint limits

## Training Pipelines

### Behavior Cloning

1. Collect expert demonstrations (scripted or teleoperated)
2. Train policy to imitate expert actions (supervised learning)
3. Evaluate on test episodes

### Reinforcement Learning

1. Define reward function in environment
2. Train policy with PPO/SAC (Stable-Baselines3)
3. Evaluate success rate and sample efficiency

## Data Flow

**Training (BC)**:
```
Expert demos → Dataset → Policy training → Checkpoint
```

**Training (RL)**:
```
Environment ↔ Policy → Replay buffer → Policy update
```

**Evaluation**:
```
Environment → Perception → Policy → Controller → Action → Environment
```

## Key Design Decisions

1. **Modular architecture**: each component is independently testable
2. **Gym interface**: standard API for RL algorithms
3. **Vision-based**: RGB input (no privileged state)
4. **Continuous control**: smooth, realistic actions
5. **Reproducible**: deterministic seeding, fixed evaluation protocol
