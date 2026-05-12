# Data Directory

This directory stores expert demonstrations and training data.

## Structure

```
data/
├── expert_pick_place.pt    # Expert demos for pick-and-place
├── expert_drawer.pt        # Expert demos for drawer task
├── expert_button.pt        # Expert demos for button task
└── README.md               # This file
```

## Data Format

Expert demonstration files are PyTorch tensors with the following structure:

```python
{
    "observations": {
        "image": torch.Tensor,        # (N, 224, 224, 3) uint8
        "proprioception": torch.Tensor, # (N, proprio_dim) float32
        "goal": torch.Tensor,          # (N, goal_dim) float32
    },
    "actions": torch.Tensor,          # (N, action_dim) float32
}
```

Where `N` is the total number of transitions across all episodes.

## Collecting Expert Data

Expert demonstrations are automatically collected when training with behavior cloning:

```bash
python train/train_bc.py --task pick_place --num_expert_episodes 100
```

This will:
1. Check if `data/expert_pick_place.pt` exists
2. If not, collect 100 episodes using scripted policy
3. Save to `data/expert_pick_place.pt`
4. Train policy on collected data

## Manual Data Collection

To collect data without training:

```python
from train.expert_data import collect_expert_data

collect_expert_data(
    task="pick_place",
    num_episodes=100,
    save_path="data/expert_pick_place.pt"
)
```

## Data Statistics

After collection, you can inspect the data:

```python
import torch

data = torch.load("data/expert_pick_place.pt")
print(f"Total transitions: {len(data['actions'])}")
print(f"Image shape: {data['observations']['image'].shape}")
print(f"Action shape: {data['actions'].shape}")
```

## Improving Expert Data Quality

The default scripted policies are simple and may not achieve high success rates. To improve:

1. **Implement better scripted policies** in `train/expert_data.py`
2. **Use teleoperation** to collect human demonstrations
3. **Filter episodes** by success (already done automatically)
4. **Augment data** with perturbations

## Custom Data

You can use your own data by creating a file with the same format:

```python
import torch
import numpy as np

# Your data collection code here
observations = {...}
actions = np.array([...])

# Save in correct format
data = {
    "observations": {
        "image": torch.from_numpy(images),
        "proprioception": torch.from_numpy(proprio),
        "goal": torch.from_numpy(goals),
    },
    "actions": torch.from_numpy(actions),
}

torch.save(data, "data/my_custom_data.pt")
```

Then train with:

```bash
python train/train_bc.py --data_path data/my_custom_data.pt
```

## Data Augmentation

To enable data augmentation during training, modify the training script or use configuration:

```yaml
# In config file
augmentation:
  enabled: true
  random_crop: true
  color_jitter: true
  random_flip: false
```

## Storage

- Each expert data file is typically 100-500 MB depending on number of episodes
- Images are stored as uint8 to save space
- Consider using compression for large datasets

## Sharing Data

If you collect high-quality demonstrations, consider sharing them:

1. Upload to cloud storage (Google Drive, S3, etc.)
2. Add download link to README
3. Document collection procedure
4. Include success rate and statistics

## Pre-trained Data

Pre-trained expert demonstrations will be available at:
- [Coming soon] Pick-and-place (1000 episodes, 80% success)
- [Coming soon] Drawer manipulation (500 episodes, 90% success)
- [Coming soon] Button press (500 episodes, 95% success)
