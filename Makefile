.PHONY: install test train-bc train-rl eval demo clean docker-build docker-run

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

# Testing
test:
	pytest tests/ -v

test-ci:
	bash scripts/ci_test.sh

# Training
train-bc:
	python train/train_bc.py --task pick_place --epochs 50

train-rl:
	python train/train_rl.py --task pick_place --algo ppo --total_timesteps 1000000

# Evaluation
eval:
	python eval.py --task pick_place --checkpoint checkpoints/bc_pick_place_final.pt --episodes 50 --render

# Demo
demo:
	python scripts/demo.py --task pick_place

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

# Docker
docker-build:
	docker build -t embodied-ai-mujoco .

docker-run:
	docker run -it --rm -v $(PWD):/workspace embodied-ai-mujoco

# Tensorboard
tensorboard:
	tensorboard --logdir runs/

# Help
help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run unit tests"
	@echo "  make test-ci      - Run full CI test suite"
	@echo "  make train-bc     - Train with behavior cloning"
	@echo "  make train-rl     - Train with reinforcement learning"
	@echo "  make eval         - Evaluate trained policy"
	@echo "  make demo         - Run demo with random policy"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make tensorboard  - Launch tensorboard"
