"""Video utilities."""
import numpy as np
import imageio
from pathlib import Path
from typing import List


def save_video(
    frames: List[np.ndarray],
    path: str,
    fps: int = 30,
    codec: str = "libx264",
):
    """
    Save frames as video.
    
    Args:
        frames: list of (H, W, 3) RGB frames
        path: output video path
        fps: frames per second
        codec: video codec
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to uint8 if needed
    frames = [
        frame.astype(np.uint8) if frame.dtype != np.uint8 else frame
        for frame in frames
    ]
    
    # Save video
    imageio.mimsave(path, frames, fps=fps, codec=codec)
