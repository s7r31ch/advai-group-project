import pandas as pd
import os
from torch.utils.data import Dataset
from PIL import Image

class TrackDataset(Dataset):
    
    label_to_num = {
        "single": 0,
        "t_left": 1,
        "t_middle": 2,
        "t_right": 3,
        "cross": 4,
        "off_track": 5
    }
    
    num_to_label = {
        0: "single",
        1: "t_left",
        2: "t_middle",
        3: "t_right",
        4: "cross",
        5: "off_track"
    }
    
    def __init__(self, 
                 dataframe, 
                 transform = None):
        self.dataframe = dataframe
        self.transform = transform
        
    def __getitem__(self, index):
        sample_path = self.dataframe.iloc[index, 0]
        label = self.label_to_num[self.dataframe.iloc[index, 1]]
        sample = Image.open(sample_path).convert("RGB")
        if self.transform: sample = self.transform(sample)
        return sample, label
    
    def __len__(self):
        return len(self.dataframe)