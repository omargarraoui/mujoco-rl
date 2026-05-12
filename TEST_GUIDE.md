# Testing Guide

## Quick Test (5 minutes)

### 1. Verify Installation
```bash
python scripts/verify_install.py
```

**Expected**: All checks pass ✓

### 2. Run Unit Tests
```bash
pytest tests/ -v
```

**Expected**: All tests pass

### 3. Test Environment Creation
```bash
python -c "from envs import PickPlaceEnv; env = PickPlaceEnv(); obs, _ = env.reset(); print('✓ Environment OK')"
```

### 4. Test Policy Creation
```bash
python -c "from policies import MLPPolicy; import torch; policy = MLPPolicy(3, 12, 3); obs = {'image': torch.randint(0, 255, (1, 224, 224, 3), dtype=torch.uint8), 'proprioception': torch.randn(1, 12), 'goal': torch.randn(1, 3)}; action = policy(obs); print('✓ Policy OK')"
```

### 5. Run Short Demo
```bash
python scripts/demo.py --task pick_place
```

**Expected**: Creates `demo_pick_place.mp4`

## Full Test Suite

```bash
# Run all CI tests
bash scripts/ci_test.sh
```

## Test Training (Optional, ~5 minutes)

```bash
# Quick training test (1 epoch)
python train/train_bc.py --task pick_place --epochs 1 --num_expert_episodes 10
```

## Troubleshooting Tests

If tests fail, check:
1. Python version >= 3.8
2. All dependencies installed
3. MuJoCo installed correctly
4. No conflicting packages

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for solutions.
