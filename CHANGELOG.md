# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release of Embodied AI MuJoCo framework
- Core environment layer with MuJoCo Gym wrapper
- Three manipulation tasks: pick-and-place, drawer, tool use
- Vision-based perception module (CNN and ViT encoders)
- MLP and RNN policy networks
- Behavior cloning training pipeline
- Reinforcement learning training (PPO/SAC via Stable-Baselines3)
- Evaluation script with deterministic metrics
- Hierarchical planner module (optional)
- Action mapper controller with safety constraints
- Comprehensive test suite
- GitHub Actions CI/CD pipeline
- Docker support
- Documentation (usage, architecture, API, troubleshooting)
- Example configurations and experiments
- Visualization tools for results

### Features
- Modular architecture with clear separation of concerns
- Reproducible training with deterministic seeding
- Batch evaluation with JSON metrics output
- Video rendering of episodes
- Tensorboard logging
- Headless mode for CI/CD
- Multi-environment parallel training

### Documentation
- README with quick start guide
- Usage guide with training examples
- Architecture documentation
- API reference
- Troubleshooting guide
- Contributing guidelines

## [Unreleased]

### Planned
- Additional manipulation tasks
- Multi-task training support
- Vision-language model integration for planning
- Improved expert data collection tools
- Pre-trained model checkpoints
- Benchmark results
- ROS interface (optional)
- Real robot deployment guide
