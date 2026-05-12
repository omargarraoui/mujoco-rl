# Quick Start Guide

Get up and running with Embodied AI MuJoCo in 5 minutes.

🌐 **[View Interactive Demo](https://omargarraoui.github.io/mujoco-rl/)** | 📚 **[Full Documentation](https://github.com/omargarraoui/mujoco-rl/tree/main/docs)**

## 1. Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/username/embodied_ai_mujoco.git
cd embodied_ai_mujoco

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Verify installation
python scripts/verify_install.py
```

**Expected output**: All checks should pass ✓

## 2. Run Demo (1 minute)

```bash
# Run demo with random policy
python scripts/demo.py --task pick_place
```

**Output**: `demo_pick_place.mp4` video file

## 3. Train Policy (30 seconds setup)

### Option A: Behavior Cloning (Fast)

```bash
# Train with behavior cloning
python train/train_bc.py --task pick_place --epochs 10
```

**Time**: ~5-10 minutes on CPU, ~2 minutes on GPU

### Option B: Reinforcement Learning (Slower but better)

```bash
# Train with PPO
python train/train_rl.py --task pick_place --algo ppo --total_timesteps 100000
```

**Time**: ~30 minutes on CPU, ~10 minutes on GPU

## 4. Evaluate (1 minute)

```bash
# Evaluate trained policy
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/bc_pick_place_final.pt \
  --episodes 10 \
  --render
```

**Output**: 
- `results/pick_place_eval.json` (metrics)
- `videos/pick_place_ep*.mp4` (videos)

## 5. Visualize Results (30 seconds)

```bash
# Plot evaluation metrics
python scripts/visualize_results.py --results results/pick_place_eval.json
```

**Output**: `results/pick_place_eval_plot.png`

---

## Common Commands

### Training

```bash
# Quick training (10 epochs)
make train-bc

# Full training (50 epochs)
python train/train_bc.py --task pick_place --epochs 50

# RL training
make train-rl
```

### Evaluation

```bash
# Quick eval (10 episodes)
python eval.py --task pick_place --checkpoint <path> --episodes 10

# Full eval with videos
make eval
```

### Testing

```bash
# Run unit tests
make test

# Run CI tests
make test-ci
```

### Monitoring

```bash
# Launch tensorboard
make tensorboard
# Open http://localhost:6006
```

---

## Next Steps

### Learn More

1. **Usage Guide**: See [docs/USAGE.md](docs/USAGE.md) for detailed instructions
2. **Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
3. **API Reference**: See [docs/API.md](docs/API.md) for code documentation

### Try Different Tasks

```bash
# Drawer manipulation
python scripts/demo.py --task drawer
python train/train_bc.py --task drawer

# Button press
python scripts/demo.py --task button
python train/train_bc.py --task button
```

### Experiment with Hyperparameters

```bash
# Use ViT encoder (better but slower)
python train/train_bc.py --vision_encoder vit

# Use RNN policy (for temporal reasoning)
python train/train_bc.py --policy_type rnn

# Larger network
python train/train_bc.py --hidden_dim 512
```

### Customize

1. **Add new task**: See [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Modify reward**: Edit `envs/<task>_env.py`
3. **Change network**: Edit `policies/mlp_policy.py`

---

## Troubleshooting

### Installation fails

```bash
# Install system dependencies (Ubuntu)
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# Verify MuJoCo
python -c "import mujoco; print(mujoco.__version__)"
```

### Training is slow

```bash
# Use simpler encoder
python train/train_bc.py --vision_encoder simple

# Reduce batch size
python train/train_bc.py --batch_size 32
```

### Low success rate

```bash
# Train longer
python train/train_bc.py --epochs 100

# Use more expert data
python train/train_bc.py --num_expert_episodes 500
```

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more solutions.

---

## Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: Open GitHub issue
- **Questions**: Use GitHub Discussions

---

## Summary

You've learned how to:
- ✅ Install the framework
- ✅ Run a demo
- ✅ Train a policy
- ✅ Evaluate performance
- ✅ Visualize results

**Total time**: ~5 minutes + training time

Ready to build embodied AI systems! 🤖
