"""Verify installation and system setup."""
import sys
import importlib


def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name}: {e}")
        return False


def check_mujoco():
    """Check MuJoCo installation."""
    try:
        import mujoco
        print(f"✓ MuJoCo {mujoco.__version__}")
        
        # Try to create a simple model
        xml = """
        <mujoco>
          <worldbody>
            <geom type="plane" size="1 1 0.1"/>
          </worldbody>
        </mujoco>
        """
        model = mujoco.MjModel.from_xml_string(xml)
        data = mujoco.MjData(model)
        print("  ✓ MuJoCo model creation OK")
        return True
    except Exception as e:
        print(f"✗ MuJoCo: {e}")
        return False


def check_torch():
    """Check PyTorch installation."""
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")
        
        # Check CUDA
        if torch.cuda.is_available():
            print(f"  ✓ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("  ⚠ CUDA not available (CPU only)")
        
        return True
    except Exception as e:
        print(f"✗ PyTorch: {e}")
        return False


def check_environments():
    """Check if environments can be created."""
    try:
        from envs import PickPlaceEnv, DrawerEnv, ToolUseEnv
        
        # Test each environment
        for env_cls, name in [
            (PickPlaceEnv, "PickPlaceEnv"),
            (DrawerEnv, "DrawerEnv"),
            (ToolUseEnv, "ToolUseEnv"),
        ]:
            env = env_cls(render_mode=None)
            obs, _ = env.reset(seed=0)
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            env.close()
            print(f"  ✓ {name} OK")
        
        return True
    except Exception as e:
        print(f"✗ Environments: {e}")
        return False


def check_policies():
    """Check if policies can be created."""
    try:
        from policies import MLPPolicy, RNNPolicy
        import torch
        
        # Test MLP policy
        policy = MLPPolicy(action_dim=3, proprio_dim=12, goal_dim=3)
        obs = {
            "image": torch.randint(0, 255, (1, 224, 224, 3), dtype=torch.uint8),
            "proprioception": torch.randn(1, 12),
            "goal": torch.randn(1, 3),
        }
        action = policy(obs)
        print(f"  ✓ MLPPolicy OK")
        
        # Test RNN policy
        policy = RNNPolicy(action_dim=3, proprio_dim=12, goal_dim=3)
        action, hidden = policy(obs)
        print(f"  ✓ RNNPolicy OK")
        
        return True
    except Exception as e:
        print(f"✗ Policies: {e}")
        return False


def main():
    """Run all checks."""
    print("="*60)
    print("Verifying Embodied AI MuJoCo Installation")
    print("="*60)
    print()
    
    print("Checking core dependencies:")
    all_ok = True
    
    # Core dependencies
    all_ok &= check_import("numpy")
    all_ok &= check_import("gymnasium")
    all_ok &= check_torch()
    all_ok &= check_mujoco()
    all_ok &= check_import("torchvision")
    all_ok &= check_import("timm")
    all_ok &= check_import("imageio")
    all_ok &= check_import("stable_baselines3", "Stable-Baselines3")
    
    print()
    print("Checking project modules:")
    all_ok &= check_import("envs")
    all_ok &= check_import("policies")
    all_ok &= check_import("perception")
    all_ok &= check_import("planner")
    all_ok &= check_import("controllers")
    
    print()
    print("Testing environment creation:")
    all_ok &= check_environments()
    
    print()
    print("Testing policy creation:")
    all_ok &= check_policies()
    
    print()
    print("="*60)
    if all_ok:
        print("✓ All checks passed! Installation is complete.")
        print()
        print("Next steps:")
        print("  1. Run demo: python scripts/demo.py --task pick_place")
        print("  2. Train policy: python train/train_bc.py --task pick_place")
        print("  3. See docs/USAGE.md for more information")
    else:
        print("✗ Some checks failed. Please install missing dependencies.")
        print()
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    print("="*60)


if __name__ == "__main__":
    main()
