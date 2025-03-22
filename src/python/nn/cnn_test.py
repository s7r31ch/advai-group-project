import torch
from torchvision import transforms
from PIL import Image
from torch import nn

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


# 加载模型
model = CNNClassifier(num_classes=5)
model.load_state_dict(torch.load("./src/resources/model.pth"))
model.eval()

# 定义图像预处理
transform = transforms.Compose([
    transforms.Resize((400, 640)),  # 调整大小
    transforms.ToTensor(),         # 转为Tensor
    transforms.Normalize((0.5,), (0.5,))  # 归一化
])

# 加载并预处理图像
image_path = "src/resources/ds_test/crossroad Image.png"
image = Image.open(image_path).convert('L')  # 灰度图
image = transform(image)
image = image.unsqueeze(0)  # 增加批次维度

# 进行推理
with torch.no_grad():
    outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    predicted_class = predicted.item()

# 映射类别索引到标签名称
label_map = {
    "single": 0,
    "t_left": 1,
    "t_middle": 2,
    "t_right": 3,
    "cross": 4
}

predicted_label = label_map[predicted_class]

print(f'预测的类别为: {predicted_label}')