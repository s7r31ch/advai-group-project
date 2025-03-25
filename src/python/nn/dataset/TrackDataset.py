import pandas as pd
import os
from torch.utils.data import Dataset
from PIL import Image

class TrackDataset(Dataset):
    
    def __init__(self, 
                 dataframe, 
                 transform = None):
        self.dataframe = dataframe
        self.transform = transform
        
    def __getitem__(self, index):
        sample_path = self.dataframe.iloc[index, 0]
        label = self.dataframe[index, 1]
        sample = Image.open(sample_path).convert("RGB")
        if self.transform: sample = self.transform(sample)
        return sample, label
    
    def __len__(self):
        return len(self.dataframe)