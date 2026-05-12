#!/bin/bash
# CI test script: comprehensive checks for GitHub Actions

set -e  # Exit on error

echo "=========================================="
echo "Running CI Tests"
echo "=========================================="

# 1. Unit tests
echo ""
echo "[1/5] Running unit tests..."
pytest tests/ -v

# 2. Environment creation
echo ""
echo "[2/5] Testing environment creation..."
python -c "from envs import PickPlaceEnv; env = PickPlaceEnv(); env.reset(); env.close(); print('✓ PickPlaceEnv OK')"
python -c "from envs import DrawerEnv; env = DrawerEnv(); env.reset(); env.close(); print('✓ DrawerEnv OK')"
python -c "from envs import ToolUseEnv; env = ToolUseEnv(); env.reset(); env.close(); print('✓ ToolUseEnv OK')"

# 3. Policy creation
echo ""
echo "[3/5] Testing policy creation..."
python -c "from policies import MLPPolicy; policy = MLPPolicy(3, 12, 3); print('✓ MLPPolicy OK')"
python -c "from policies import RNNPolicy; policy = RNNPolicy(3, 12, 3); print('✓ RNNPolicy OK')"

# 4. Short rollouts
echo ""
echo "[4/5] Running short rollouts..."
python scripts/test_rollout.py --episodes 2 --max_steps 10

# 5. Import checks
echo ""
echo "[5/5] Checking all imports..."
python -c "from perception import VisionEncoder, SimpleConvEncoder; print('✓ Perception OK')"
python -c "from planner import HierarchicalPlanner; print('✓ Planner OK')"
python -c "from controllers import ActionMapper; print('✓ Controllers OK')"

echo ""
echo "=========================================="
echo "All CI tests passed! ✓"
echo "=========================================="
