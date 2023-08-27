from pathlib import Path
import os
import torchvision
import torch
import numpy as np
from torchvision.transforms import ToTensor
from PIL import Image

class CarlaDataset(torch.utils.data.Dataset):
    def __init__(self, root, transform=None, target_transform=None):
        self.root = root 
        self.sub_dirs = os.listdir(path=root)
        self.data = {}
        for dir in self.sub_dirs:
            path = os.path.join(self.root, dir)
            self.data[dir] = os.listdir(path) 
        self.transform = transform
        self.target_transform = target_transform
        
    def __getitem__(self, i):
        items = {}
        for key, vals in self.data.items():
            x = Image.open(os.path.join(self.root, key, vals[i]))
            if self.transform:
                x = self.transform(x)
            items[key] = x
        return items

    def __len__(self):
        if len(self.data) != 0:
            return len(next(iter(self.data.values())))
        else:
            return 0
