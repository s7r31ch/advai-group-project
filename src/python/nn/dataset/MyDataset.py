from torch.utils.data import Dataset
from nn.dataset.LabelMapper import LabelMapper
import pandas as pd
import os
from PIL import Image
from nn.dataset.Preprocessing import Preprocessing

class MyDataset(Dataset):
    
    def __init__(self, csv_file, img_dir, transform=None):

        self.labels_define = pd.read_csv(csv_file, header=None, names=["filename", "label"])
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.labels_define)

    def __getitem__(self, idx):
        # 获取当前索引对应的图像文件名和标签
        img_name = self.labels_define.iloc[idx, 0]
        cat = LabelMapper.label_to_cat[self.labels_define.iloc[idx, 1]]
        img_path = os.path.join(self.img_dir, img_name)
        # 以灰度模式加载图像
        image = Image.open(img_path).convert('L')
        image = Preprocessing.transform_0(image)
        return image, cat
