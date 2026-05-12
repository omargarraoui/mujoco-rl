# Project Structure

Complete overview of the Embodied AI MuJoCo repository structure.

```
embodied_ai_mujoco/
│
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── CHANGELOG.md               # Version history
├── ROADMAP.md                 # Future development plans
├── CONTRIBUTING.md            # Contribution guidelines
├── Makefile                   # Common commands
├── Dockerfile                 # Container setup
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── setup.py                   # Package setup
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── PROJECT_STRUCTURE.md       # This file
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
│
├── config/
│   └── default.yaml           # Default configuration
│
├── docs/
│   ├── USAGE.md               # Usage guide
│   ├── ARCHITECTURE.md        # System architecture
│   ├── API.md                 # API reference
│   └── TROUBLESHOOTING.md     # Common issues and solutions
│
├── envs/                      # Environment layer
│   ├── __init__.py
│   ├── base_env.py            # Base MuJoCo environment
│   ├── pick_place_env.py      # Pick and place task
│   ├── drawer_env.py          # Drawer manipulation
│   ├── tool_use_env.py        # Tool use tasks
│   └── assets/                # MuJoCo XML scenes
│       ├── pick_place.xml
│       ├── drawer.xml
│       └── button.xml
│
├── perception/                # Perception module
│   ├── __init__.py
│   └── vision_encoder.py      # Vision encoders (CNN/ViT)
│
├── policies/                  # Policy networks
│   ├── __init__.py
│   ├── mlp_policy.py          # Feedforward policy
│   └── rnn_policy.py          # Recurrent policy
│
├── planner/                   # Planning module (optional)
│   ├── __init__.py
│   └── hierarchical_planner.py # Goal decomposition
│
├── controllers/               # Control layer
│   ├── __init__.py
│   └── action_mapper.py       # Action mapping and safety
│
├── train/                     # Training scripts
│   ├── __init__.py
│   ├── train_bc.py            # Behavior cloning
│   ├── train_rl.py            # Reinforcement learning
│   ├── expert_data.py         # Expert data collection
│   └── wrappers.py            # Gym wrappers
│
├── eval.py                    # Evaluation script
│
├── scripts/                   # Utility scripts
│   ├── __init__.py
│   ├── demo.py                # Demo visualization
│   ├── test_rollout.py        # CI rollout tests
│   ├── verify_install.py      # Installation verification
│   ├── visualize_results.py   # Results visualization
│   └── ci_test.sh             # CI test script
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_envs.py           # Environment tests
│   └── test_policies.py       # Policy tests
│
├── experiments/               # Experiment configurations
│   ├── README.md              # Experiment guide
│   └── example_config.yaml    # Example configuration
│
├── tasks/                     # Task definitions
│   └── __init__.py
│
└── utils/                     # Utilities
    ├── __init__.py
    ├── logging.py             # Logging utilities
    └── video.py               # Video utilities
```

## Module Descriptions

### Core Modules

**envs/**: MuJoCo environment wrappers
- Gym-compatible interface
- RGB + proprioception observations
- Continuous action space
- Task-specific reward functions

**perception/**: Vision processing
- CNN encoder (lightweight)
- ViT encoder (pretrained)
- Image → embedding conversion

**policies/**: Decision-making networks
- MLP policy (feedforward)
- RNN policy (temporal reasoning)
- PyTorch implementations

**planner/**: High-level planning (optional)
- Goal decomposition
- Subgoal generation
- Can integrate LLM/VLM

**controllers/**: Low-level control
- Action mapping
- Safety constraints
- Smoothing/filtering

### Training & Evaluation

**train/**: Training pipelines
- Behavior cloning (imitation)
- Reinforcement learning (PPO/SAC)
- Expert data collection
- Gym wrappers

**eval.py**: Evaluation protocol
- Deterministic metrics
- Batch evaluation
- Video rendering
- JSON results

### Development

**tests/**: Unit tests
- Environment tests
- Policy tests
- Pytest framework

**scripts/**: Utilities
- Demo visualization
- Installation verification
- Results visualization
- CI testing

**experiments/**: Experiment management
- Configuration files
- Results tracking
- Baseline comparisons

### Documentation

**docs/**: Comprehensive documentation
- Usage guide
- Architecture overview
- API reference
- Troubleshooting

### Configuration

**config/**: Default configurations
- Environment settings
- Training hyperparameters
- Evaluation parameters

## File Counts

- Python files: ~30
- MuJoCo XML scenes: 3
- Documentation files: 8
- Configuration files: 4
- Test files: 2

## Key Entry Points

1. **Training**: `train/train_bc.py`, `train/train_rl.py`
2. **Evaluation**: `eval.py`
3. **Demo**: `scripts/demo.py`
4. **Testing**: `pytest tests/`
5. **Verification**: `scripts/verify_install.py`

## Generated Directories (not in repo)

During usage, these directories are created:

```
checkpoints/    # Saved model checkpoints
runs/           # Tensorboard logs
videos/         # Rendered episode videos
results/        # Evaluation metrics (JSON)
data/           # Expert demonstrations
logs/           # Training logs
```

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- mujoco >= 3.0.0
- gymnasium >= 0.29.0
- torch >= 2.0.0
- stable-baselines3 >= 2.1.0
- timm >= 0.9.0
