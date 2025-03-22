import os
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

# 自定义 Dataset，用于加载图像和标签
class MyDataset(Dataset):
    def __init__(self, csv_file, img_dir, transform=None):
        """
        Args:
            csv_file (string): 标签文件路径，格式：{图片文件名},{标签}
            img_dir (string): 训练集图像所在文件夹路径
            transform (callable, optional): 对图像进行的转换操作
        """
        self.labels_df = pd.read_csv(csv_file, header=None, names=["filename", "label"])
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.labels_df)

    def __getitem__(self, idx):
        # 获取当前索引对应的图像文件名和标签
        img_name = self.labels_df.iloc[idx, 0]
        label = int(self.labels_df.iloc[idx, 1])
        img_path = os.path.join(self.img_dir, img_name)
        # 以灰度模式加载图像
        image = Image.open(img_path).convert('L')
        if self.transform:
            image = self.transform(image)
        return image, label

# 定义图像预处理操作
transform = transforms.Compose([
    # 这里假设图片尺寸已经是640x400，如果需要调整，请修改此处
    transforms.Resize((400, 640)),
    transforms.ToTensor(),  # 将图像转换为Tensor，并归一化到[0,1]
    transforms.Normalize((0.5,), (0.5,))  # 对灰度图进行归一化（均值0.5，标准差0.5）
])

# 实例化数据集和 DataLoader
dataset = MyDataset(csv_file="./src/resources/label.csv",
                    img_dir="./src/resources/downcam",
                    transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)

# 定义一个简单的 CNN 网络
class CNNClassifier(nn.Module):
    def __init__(self, num_classes=5):
        super(CNNClassifier, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),  # 输入通道1，输出16
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (16, 200, 320)

            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (32, 100, 160)

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)   # (64, 50, 80)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 50 * 80, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# 设置设备（GPU或CPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNNClassifier(num_classes=5).to(device)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 训练循环
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in dataloader:
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
    epoch_loss = running_loss / len(dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")

print("训练完成")
