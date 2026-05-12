import torch
import torch.nn as nn
import timm
from typing import Optional


class VisionEncoder(nn.Module):
    """Vision encoder using pretrained ViT backbone."""
    
    def __init__(
        self,
        model_name: str = "vit_small_patch16_224",
        pretrained: bool = True,
        embedding_dim: int = 256,
        freeze_backbone: bool = False,
    ):
        super().__init__()
        
        # Load pretrained ViT
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,  # Remove classification head
        )
        
        # Freeze backbone if requested
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # Get backbone output dimension
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 224, 224)
            backbone_dim = self.backbone(dummy_input).shape[-1]
        
        # Projection head
        self.projection = nn.Sequential(
            nn.Linear(backbone_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim),
        )
        
        self.embedding_dim = embedding_dim
    
    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Encode image to embedding.
        
        Args:
            image: (B, 3, H, W) tensor, values in [0, 1]
        
        Returns:
            embedding: (B, embedding_dim) tensor
        """
        # Normalize image (ImageNet stats)
        mean = torch.tensor([0.485, 0.456, 0.406], device=image.device).view(1, 3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225], device=image.device).view(1, 3, 1, 1)
        image = (image - mean) / std
        
        # Extract features
        features = self.backbone(image)
        
        # Project to embedding space
        embedding = self.projection(features)
        
        return embedding


class SimpleConvEncoder(nn.Module):
    """Lightweight CNN encoder for faster training."""
    
    def __init__(self, embedding_dim: int = 256):
        super().__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, stride=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, embedding_dim),
            nn.ReLU(),
        )
        
        self.embedding_dim = embedding_dim
    
    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Encode image to embedding.
        
        Args:
            image: (B, 3, H, W) tensor, values in [0, 1]
        
        Returns:
            embedding: (B, embedding_dim) tensor
        """
        x = self.conv(image)
        embedding = self.fc(x)
        return embedding
