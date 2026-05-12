# Troubleshooting Guide

## Installation Issues

### MuJoCo Installation Fails

**Problem**: `pip install mujoco` fails or MuJoCo doesn't render.

**Solutions**:
1. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
```

2. For macOS:
```bash
brew install glfw3
```

3. Verify installation:
```bash
python -c "import mujoco; print(mujoco.__version__)"
```

### PyTorch CUDA Issues

**Problem**: PyTorch doesn't detect GPU.

**Solutions**:
1. Check CUDA availability:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

2. Install correct PyTorch version for your CUDA:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

3. Verify GPU:
```bash
nvidia-smi
```

### Import Errors

**Problem**: `ModuleNotFoundError` when importing project modules.

**Solutions**:
1. Install in editable mode:
```bash
pip install -e .
```

2. Check Python path:
```bash
python -c "import sys; print(sys.path)"
```

3. Run from project root directory.

## Training Issues

### Out of Memory (OOM)

**Problem**: Training crashes with CUDA OOM error.

**Solutions**:
1. Reduce batch size:
```bash
python train/train_bc.py --batch_size 32
```

2. Use simpler vision encoder:
```bash
python train/train_bc.py --vision_encoder simple
```

3. Reduce number of parallel environments:
```bash
python train/train_rl.py --num_envs 2
```

4. Use CPU:
```bash
CUDA_VISIBLE_DEVICES="" python train/train_bc.py
```

### Training is Slow

**Problem**: Training takes too long.

**Solutions**:
1. Use GPU if available
2. Reduce image size in environment
3. Use simpler vision encoder (CNN instead of ViT)
4. Increase frame skip
5. Use fewer expert episodes for BC

### Low Success Rate

**Problem**: Trained policy has low success rate.

**Solutions**:
1. **Increase training time**:
   - BC: more epochs or expert episodes
   - RL: more timesteps

2. **Tune hyperparameters**:
   - Learning rate: try 1e-4, 3e-4, 1e-3
   - Batch size: 32, 64, 128
   - Hidden dim: 128, 256, 512

3. **Improve reward function**:
   - Add dense rewards
   - Tune reward scaling
   - Add success bonus

4. **Better expert data** (BC):
   - Collect more demonstrations
   - Improve expert policy quality
   - Filter failed episodes

5. **Use RNN policy** for temporal tasks:
```bash
python train/train_bc.py --policy_type rnn
```

## Environment Issues

### Simulation Instability

**Problem**: Robot falls or simulation explodes.

**Solutions**:
1. Check action clipping is enabled
2. Reduce action scale in controller
3. Increase damping in MuJoCo XML
4. Add safety constraints
5. Reduce frame skip

### Rendering Issues

**Problem**: Rendering doesn't work or is slow.

**Solutions**:
1. For headless mode (no display):
```bash
export MUJOCO_GL=osmesa  # or egl
```

2. For slow rendering:
   - Reduce image size
   - Use `render_mode=None` during training
   - Only render during evaluation

3. For X11 errors on remote server:
```bash
xvfb-run -a python scripts/demo.py --task pick_place
```

## Evaluation Issues

### Inconsistent Results

**Problem**: Evaluation results vary between runs.

**Solutions**:
1. Use fixed seed:
```bash
python eval.py --seed 42
```

2. Increase number of episodes:
```bash
python eval.py --episodes 100
```

3. Check for non-deterministic operations in policy

### Video Saving Fails

**Problem**: Videos are not saved or corrupted.

**Solutions**:
1. Install ffmpeg:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

2. Install imageio-ffmpeg:
```bash
pip install imageio-ffmpeg
```

3. Check disk space

## CI/CD Issues

### GitHub Actions Fails

**Problem**: CI tests fail on GitHub Actions.

**Solutions**:
1. Check logs in Actions tab
2. Test locally with:
```bash
bash scripts/ci_test.sh
```

3. Common issues:
   - Missing system dependencies
   - Headless rendering not configured
   - Tests timeout (reduce test episodes)

### Tests Pass Locally but Fail in CI

**Problem**: Tests work on your machine but not in CI.

**Solutions**:
1. Use Docker to replicate CI environment:
```bash
docker build -t embodied-ai-mujoco .
docker run -it embodied-ai-mujoco bash scripts/ci_test.sh
```

2. Check for:
   - Hardcoded paths
   - Missing dependencies in requirements.txt
   - Non-deterministic behavior

## Performance Issues

### Slow Environment Steps

**Problem**: Environment step() is slow.

**Solutions**:
1. Increase frame skip
2. Reduce image resolution
3. Use simpler MuJoCo scene
4. Profile with:
```python
import cProfile
cProfile.run('env.step(action)')
```

### Slow Policy Inference

**Problem**: Policy forward pass is slow.

**Solutions**:
1. Use smaller network
2. Use simple CNN instead of ViT
3. Batch observations
4. Use GPU
5. Profile with:
```python
import torch.profiler
```

## Getting Help

If you can't resolve an issue:

1. Check existing GitHub issues
2. Run verification script:
```bash
python scripts/verify_install.py
```

3. Open a new issue with:
   - Error message and full traceback
   - System information (OS, Python version, GPU)
   - Steps to reproduce
   - Output of `pip list`

4. For questions, use GitHub Discussions
