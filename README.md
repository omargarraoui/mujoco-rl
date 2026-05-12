# Embodied AI in MuJoCo

[![CI](https://github.com/omargarraoui/mujoco-rl/workflows/CI/badge.svg)](https://github.com/omargarraoui/mujoco-rl/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Sistema modulare di embodied AI per task di manipolazione fisica in simulazione MuJoCo con pipeline completa **perception → planning → policy → control**.

📚 **[Documentation](https://github.com/omargarraoui/mujoco-rl/tree/main/docs)** | 🚀 **[Quick Start](QUICKSTART.md)** | 🎯 **[START HERE](START_HERE.md)**

## Features

✅ **Modular architecture**: separazione chiara tra perception, policy, planning, control  
✅ **Multiple tasks**: pick-and-place, drawer manipulation, tool use  
✅ **Vision-based**: RGB input con encoder CNN/ViT  
✅ **Training methods**: behavior cloning + reinforcement learning (PPO/SAC)  
✅ **Reproducible**: deterministic seeding, batch evaluation  
✅ **CI/CD**: automated testing con GitHub Actions  

## Architecture

```
┌─────────────┐
│ Environment │ MuJoCo Gym wrapper
└──────┬──────┘
       │ RGB + proprioception + goal
       ▼
┌─────────────┐
│ Perception  │ Vision encoder (CNN/ViT)
└──────┬──────┘
       │ visual embedding
       ▼
┌─────────────┐
│   Policy    │ PyTorch network (MLP/RNN)
└──────┬──────┘
       │ action [-1, 1]
       ▼
┌─────────────┐
│ Controller  │ Action mapping + safety
└──────┬──────┘
       │ actuator commands
       ▼
┌─────────────┐
│   MuJoCo    │ Physics simulation
└─────────────┘
```

## Quick Start

**New to the project?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute tutorial.

### Installation

```bash
git clone https://github.com/username/embodied_ai_mujoco.git
cd embodied_ai_mujoco

# Automated setup
bash scripts/setup.sh

# Or manual installation
pip install -r requirements.txt
pip install -e .
```

**Detailed instructions**: See [INSTALLATION.md](INSTALLATION.md)

### Run Demo

```bash
# Random policy demo
python scripts/demo.py --task pick_place
```

### Train Policy

```bash
# Behavior cloning
python train/train_bc.py --task pick_place --epochs 50

# Reinforcement learning (PPO)
python train/train_rl.py --task pick_place --algo ppo --total_timesteps 1000000
```

### Evaluate

```bash
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/bc_pick_place_final.pt \
  --episodes 50 \
  --render
```

Output: `results/pick_place_eval.json` con success rate, avg steps, reward.

## Supported Tasks

| Task | Description | Goal |
|------|-------------|------|
| `pick_place` | Pick object and place at target | 3D target position |
| `drawer` | Open/close drawer | Drawer opening amount |
| `button` | Press button with tool | Button activation |

## Training Methods

### 1. Behavior Cloning (Imitation Learning)

```bash
python train/train_bc.py \
  --task pick_place \
  --policy_type mlp \
  --vision_encoder simple \
  --epochs 50 \
  --batch_size 64
```

Collects expert demonstrations (scripted policy) and trains via supervised learning.

### 2. Reinforcement Learning

```bash
python train/train_rl.py \
  --task pick_place \
  --algo ppo \
  --num_envs 4 \
  --total_timesteps 1000000
```

Trains policy with PPO or SAC using Stable-Baselines3.

## Evaluation Protocol

```bash
python eval.py --task pick_place --checkpoint <path> --episodes 50
```

**Metrics**:
- Success rate (%)
- Average steps to completion
- Average episode reward
- Per-episode details (JSON)

**Deterministic**: fixed seeds for reproducibility.

## Repository Structure

```
embodied_ai_mujoco/
├── envs/               # MuJoCo environments
│   ├── base_env.py
│   ├── pick_place_env.py
│   ├── drawer_env.py
│   ├── tool_use_env.py
│   └── assets/         # MuJoCo XML scenes
├── perception/         # Vision encoders
│   └── vision_encoder.py
├── policies/           # Policy networks
│   ├── mlp_policy.py
│   └── rnn_policy.py
├── planner/            # High-level planning (optional)
│   └── hierarchical_planner.py
├── controllers/        # Action mapping
│   └── action_mapper.py
├── train/              # Training scripts
│   ├── train_bc.py
│   ├── train_rl.py
│   └── expert_data.py
├── eval.py             # Evaluation script
├── scripts/            # Utilities
│   ├── demo.py
│   ├── test_rollout.py
│   └── verify_install.py
├── tests/              # Unit tests
├── docs/               # Documentation
└── .github/workflows/  # CI configuration
    └── ci.yml          # Testing pipeline
```

## CI/CD

GitHub Actions runs on every push:
- Unit tests (pytest)
- Environment creation checks
- Policy instantiation tests
- Short rollout tests (headless)
- Deterministic seed verification

No long training in CI (only smoke tests).

## Documentation

- [Usage Guide](docs/USAGE.md) - detailed training/evaluation instructions
- [Architecture](docs/ARCHITECTURE.md) - system design and data flow

## Requirements

- Python ≥ 3.8
- MuJoCo ≥ 3.0
- PyTorch ≥ 2.0
- Gymnasium ≥ 0.29
- Stable-Baselines3 ≥ 2.1

See `requirements.txt` for full list.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure CI passes
5. Submit pull request

## License

MIT License - see [LICENSE](LICENSE) file.

## Citation

```bibtex
@software{embodied_ai_mujoco,
  title={Embodied AI in MuJoCo},
  author={Your Name},
  year={2024},
  url={https://github.com/username/embodied_ai_mujoco}
}
```

## Acknowledgments

- MuJoCo physics engine
- Stable-Baselines3 for RL algorithms
- timm for vision models
