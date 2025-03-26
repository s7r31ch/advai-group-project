import torch.nn as nn
import torch.nn.functional as F

class TrackCNN(nn.Module):
    
    NETWORK_NAME = "TrackCNN"
    
    def __init__(self, num_labels):
        super(TrackCNN, self).__init__()
        
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 池化层：尺寸减半
        
        # 卷积层1：输入3通道，输出32通道，卷积核大小3×3
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)                  # 批归一化，加速收敛
        
        # 卷积层2：32通道 → 64通道
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        
        # 卷积层3：64通道 → 128通道
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        # 全连接层（FC）
        # 128通道，特征图大小为 128/8 = 16 → 128*16*16 = 32768
        self.fc1 = nn.Linear(128 * 16 * 16, 512)
        self.fc2 = nn.Linear(512, num_labels)
    
    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        
        # 展平
        x = x.view(x.size(0), -1)  # 将多维张量展平成一维张量
        
        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
