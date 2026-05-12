# Experiments

This directory contains experiment configurations and results.

## Running Experiments

### Using Config Files

```bash
# Train with config
python train/train_bc.py --config experiments/example_config.yaml

# Evaluate with config
python eval.py --config experiments/example_config.yaml
```

### Experiment Tracking

Organize experiments by task and method:

```
experiments/
├── pick_place/
│   ├── bc_baseline.yaml
│   ├── bc_vit.yaml
│   ├── ppo_baseline.yaml
│   └── results/
├── drawer/
│   ├── bc_baseline.yaml
│   └── results/
└── button/
    └── ...
```

## Baseline Results

### Pick and Place

| Method | Vision | Success Rate | Avg Steps | Training Time |
|--------|--------|--------------|-----------|---------------|
| BC | CNN | TBD | TBD | TBD |
| BC | ViT | TBD | TBD | TBD |
| PPO | CNN | TBD | TBD | TBD |
| SAC | CNN | TBD | TBD | TBD |

### Drawer Open

| Method | Vision | Success Rate | Avg Steps | Training Time |
|--------|--------|--------------|-----------|---------------|
| BC | CNN | TBD | TBD | TBD |
| PPO | CNN | TBD | TBD | TBD |

### Button Press

| Method | Vision | Success Rate | Avg Steps | Training Time |
|--------|--------|--------------|-----------|---------------|
| BC | CNN | TBD | TBD | TBD |
| PPO | CNN | TBD | TBD | TBD |

## Reproducing Results

1. Train policy:
```bash
python train/train_bc.py --config experiments/pick_place/bc_baseline.yaml
```

2. Evaluate:
```bash
python eval.py \
  --task pick_place \
  --checkpoint checkpoints/pick_place_bc/final.pt \
  --episodes 100 \
  --render
```

3. Visualize results:
```bash
python scripts/visualize_results.py --results results/pick_place_eval.json
```

## Hyperparameter Tuning

Key hyperparameters to tune:

**Policy**:
- `hidden_dim`: network capacity
- `vision_encoder`: simple (fast) vs vit (accurate)
- `policy_type`: mlp (stateless) vs rnn (temporal)

**Training**:
- `learning_rate`: 1e-4 to 1e-3
- `batch_size`: 32 to 256
- `num_expert_episodes`: 50 to 500 (BC)

**Environment**:
- `frame_skip`: 1 to 10 (control frequency)
- `reward_scale`: task-specific

## Adding New Experiments

1. Copy `example_config.yaml`
2. Modify parameters
3. Run training
4. Document results in this README
