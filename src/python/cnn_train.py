
from nn.dataset.MyDataset import MyDataset
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from nn.network.MyCNN import MyCNN
from python.nn.dataset.Preprocessing import Preprocessing
from utils.LogUtils import LogUtils


# 实例化数据集和 DataLoader
dataset = MyDataset(csv_file="./src/resources/label.csv",
                    img_dir="./src/resources/ds_train/",
                    transform=Preprocessing.transform_0)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=0)



# 设置设备（GPU或CPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyCNN(num_classes=5).to(device)

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

model_dir = "./src/resources/"
model_name = "model_" + LogUtils.get_model_name_timestamp()
model_ext = ".pth"
model_path = model_dir + model_name + model_ext
torch.save(model.state_dict(), model_path)

print("训练完成")
