#!/bin/bash
# Setup script for Embodied AI MuJoCo

set -e

echo "=========================================="
echo "Embodied AI MuJoCo - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "Error: Python 3.8 or higher required"
    exit 1
fi
echo "✓ Python version OK"
echo ""

# Install dependencies
echo "[2/5] Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Install package
echo "[3/5] Installing package in editable mode..."
pip install -e .
echo "✓ Package installed"
echo ""

# Create directories
echo "[4/5] Creating directories..."
mkdir -p checkpoints
mkdir -p runs
mkdir -p videos
mkdir -p results
mkdir -p data
mkdir -p logs
echo "✓ Directories created"
echo ""

# Verify installation
echo "[5/5] Verifying installation..."
python scripts/verify_install.py
echo ""

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run demo: python scripts/demo.py --task pick_place"
echo "  2. Train policy: python train/train_bc.py --task pick_place"
echo "  3. See QUICKSTART.md for more information"
echo ""
