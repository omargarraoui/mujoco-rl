# Contributing Guide

Thank you for considering contributing to Embodied AI MuJoCo!

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/embodied_ai_mujoco.git
cd embodied_ai_mujoco
```

2. Install in development mode:
```bash
pip install -r requirements.txt
pip install -e .
```

3. Install development dependencies:
```bash
pip install pytest pytest-cov black flake8 mypy
```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to all public functions/classes
- Keep functions focused and modular

Format code with black:
```bash
black .
```

Check style with flake8:
```bash
flake8 --max-line-length=100 --ignore=E203,W503
```

## Testing

Run tests before submitting PR:
```bash
pytest tests/ -v
```

Add tests for new functionality in `tests/`.

## Pull Request Process

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "Add feature: description"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Open a pull request with:
   - Clear description of changes
   - Reference to related issues
   - Test results
   - Screenshots/videos if applicable

5. Ensure CI passes

## Adding New Tasks

To add a new manipulation task:

1. Create MuJoCo XML scene in `envs/assets/your_task.xml`
2. Implement environment class in `envs/your_task_env.py`:
   - Inherit from `MuJoCoManipulationEnv`
   - Override `_reset_task()`, `_compute_reward()`, `_check_terminated()`
3. Add to `envs/__init__.py`
4. Add tests in `tests/test_envs.py`
5. Update documentation

## Adding New Policy Types

1. Implement policy in `policies/your_policy.py`
2. Follow interface: `forward(obs) -> action`
3. Add tests in `tests/test_policies.py`
4. Update training scripts to support new policy

## Documentation

Update documentation when adding features:
- README.md for high-level changes
- docs/USAGE.md for usage instructions
- docs/ARCHITECTURE.md for design changes
- Docstrings in code

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about implementation
- Discussion of design decisions

## Code of Conduct

Be respectful and constructive in all interactions.
