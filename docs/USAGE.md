# Usage Guide

## Installation

```bash
# Clone repository
git clone <repo-url>
cd embodied_ai_mujoco

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

## Quick Start

### 1. Test Environment

```bash
python -c "from envs import PickPlaceEnv; env = PickPlaceEnv(); env.reset(); env.close()"
```

### 2. Run Demo with Random Policy

```bash
python scripts/demo.py --task pick_place
```

This creates `demo_pick_place.mp4` showing a random policy.

### 3. Train Policy (Behavior Cloning)

```bash
# Collect expert data and train
python train/train_bc.py --task pick_place --epochs 50

# Checkpoint saved to: checkpoints/bc_pick_place_final.pt
```

### 4. Train Policy (Reinforcement Learning)

```bash
# Train with PPO
python train/train_rl.py --task pick_place --algo ppo --total_timesteps 1000000

# Train with SAC
python train/train_rl.py --task pick_place --algo sac --total_timesteps 500000
```

### 5. Evaluate Trained Policy

```bash
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/bc_pick_place_final.pt \
  --episodes 50 \
  --render
```

Results saved to `results/pick_place_eval.json` and videos to `videos/`.

## Training Options

### Behavior Cloning

```bash
python train/train_bc.py \
  --task pick_place \
  --policy_type mlp \
  --vision_encoder simple \
  --hidden_dim 256 \
  --epochs 50 \
  --batch_size 64 \
  --lr 3e-4
```

**Arguments**:
- `--task`: task name (pick_place, drawer, button)
- `--policy_type`: mlp or rnn
- `--vision_encoder`: simple (CNN) or vit (ViT)
- `--hidden_dim`: network hidden dimension
- `--epochs`: training epochs
- `--batch_size`: batch size
- `--lr`: learning rate

### Reinforcement Learning

```bash
python train/train_rl.py \
  --task pick_place \
  --algo ppo \
  --num_envs 4 \
  --total_timesteps 1000000 \
  --lr 3e-4
```

**Arguments**:
- `--algo`: ppo or sac
- `--num_envs`: parallel environments
- `--total_timesteps`: total training steps
- `--lr`: learning rate

## Evaluation

```bash
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/bc_pick_place_final.pt \
  --policy_type mlp \
  --episodes 50 \
  --render
```

**Metrics**:
- Success rate (%)
- Average steps to completion
- Average reward
- Per-episode details (JSON)

## Custom Tasks

To add a new task:

1. Create MuJoCo XML scene in `envs/assets/`
2. Implement environment class in `envs/` (inherit from `MuJoCoManipulationEnv`)
3. Override:
   - `_reset_task()`: initialize task state
   - `_compute_reward()`: define reward function
   - `_check_terminated()`: success condition
   - `_get_info()`: metrics
4. Register in `envs/__init__.py`

## Monitoring Training

```bash
# Launch tensorboard
tensorboard --logdir runs/

# View at http://localhost:6006
```

## Troubleshooting

**MuJoCo not rendering**:
- Set `render_mode=None` for headless mode
- Install OpenGL libraries: `sudo apt-get install libgl1-mesa-glx`

**Out of memory**:
- Reduce `--batch_size`
- Use `--vision_encoder simple` instead of `vit`
- Reduce `--num_envs`

**Low success rate**:
- Increase training time
- Tune reward function
- Collect more expert demonstrations
- Use curriculum learning
