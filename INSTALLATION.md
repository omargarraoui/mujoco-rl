# Installation Guide

Complete installation instructions for Embodied AI MuJoCo.

## Prerequisites

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, or Windows (WSL recommended)
- **GPU**: Optional but recommended (CUDA 11.8+ for PyTorch)

## Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/username/embodied_ai_mujoco.git
cd embodied_ai_mujoco

# Run setup script
bash scripts/setup.sh
```

This will:
1. Check Python version
2. Install dependencies
3. Install package
4. Create directories
5. Verify installation

### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/username/embodied_ai_mujoco.git
cd embodied_ai_mujoco

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .

# Verify installation
python scripts/verify_install.py
```

## System-Specific Instructions

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg

# Install Python dependencies
pip install -r requirements.txt
pip install -e .
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install glfw3 ffmpeg

# Install Python dependencies
pip install -r requirements.txt
pip install -e .
```

### Windows (WSL)

```bash
# Use Ubuntu instructions in WSL
# Or use Docker (see below)
```

## GPU Support (Optional)

### CUDA 11.8

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### CUDA 12.1

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Verify GPU

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## Docker Installation (Alternative)

### Build Image

```bash
docker build -t embodied-ai-mujoco .
```

### Run Container

```bash
docker run -it --rm \
    --gpus all \
    -v $(pwd):/workspace \
    embodied-ai-mujoco
```

### Run with X11 (for rendering)

```bash
xhost +local:docker
docker run -it --rm \
    --gpus all \
    -v $(pwd):/workspace \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    embodied-ai-mujoco
```

## Virtual Environment (Recommended)

### Using venv

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Using conda

```bash
# Create environment
conda create -n embodied-ai python=3.10

# Activate
conda activate embodied-ai

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Verification

After installation, verify everything works:

```bash
# Run verification script
python scripts/verify_install.py
```

Expected output:
```
✓ numpy
✓ gymnasium
✓ PyTorch 2.x.x
✓ MuJoCo 3.x.x
✓ All checks passed!
```

## Troubleshooting

### MuJoCo Installation Issues

**Problem**: MuJoCo fails to install or render

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# macOS
brew install glfw3

# Verify
python -c "import mujoco; print(mujoco.__version__)"
```

### PyTorch CUDA Issues

**Problem**: PyTorch doesn't detect GPU

**Solution**:
```bash
# Check CUDA version
nvidia-smi

# Install matching PyTorch version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Import Errors

**Problem**: `ModuleNotFoundError` when importing

**Solution**:
```bash
# Reinstall in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Permission Errors

**Problem**: Permission denied when installing

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development Installation

For development with additional tools:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .
pip install pytest pytest-cov black flake8 mypy

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Minimal Installation

For minimal installation (no RL, no ViT):

```bash
# Install only core dependencies
pip install mujoco>=3.0.0 gymnasium>=0.29.0 numpy>=1.24.0 torch>=2.0.0
pip install -e .
```

## Uninstallation

```bash
# Uninstall package
pip uninstall embodied_ai_mujoco

# Remove virtual environment
rm -rf venv/

# Remove generated files
rm -rf checkpoints/ runs/ videos/ results/ data/ logs/
```

## Next Steps

After successful installation:

1. **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
2. **Run Demo**: `python scripts/demo.py --task pick_place`
3. **Train Policy**: `python train/train_bc.py --task pick_place`
4. **Read Docs**: See [docs/USAGE.md](docs/USAGE.md)

## Getting Help

- **Installation Issues**: See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **GitHub Issues**: Open an issue with installation logs
- **Discussions**: Use GitHub Discussions for questions
