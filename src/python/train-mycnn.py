import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from utils.DatasetUtils import DatasetUtils
from nn.dataset.MyDataset import MyDataset
from nn.dataset.Preprocessing import Preprocessing
from nn.network.MyCNN import MyCNN
from devtoolkit.Log4P import Log4P

if __name__ == "__main__":
    
    # 有重要参数设置的预感，敬请见证
    LABEL_FILE_PATH = "src/resources/label.csv"
    DATASET_DIR = "src/resources/ds_train"
    BATCH_SIZE = 32
    NUM_EPOCHS = 10
    MODEL_SAV_PATH = "src/resources/mycnn-20250326.pth"
    LOG_FILE_PATH = "src/resources/train-log-mycnn.log"
    
    logger = Log4P(enable_level = True,
                   enable_timestamp = True,
                   enable_source = True,
                   enable_log_file = True,
                   source = "train-mycnn",
                   log_file_path = LOG_FILE_PATH)
    
    dataset = MyDataset(csv_file = LABEL_FILE_PATH,
                        img_dir = DATASET_DIR,
                        transform = Preprocessing.transform_0)
    
    train_size = int(0.8*len(dataset))
    valid_size = len(dataset) - train_size
    
    dataset_train, dataset_valid = torch.utils.data.random_split(dataset, [train_size, valid_size])
    
    dataloader_train = DataLoader(dataset = dataset_train,
                                  batch_size = BATCH_SIZE,
                                  shuffle = True,
                                  num_workers = 6)
    
    dataloader_valid = DataLoader(dataset = dataset_valid,
                                  batch_size = BATCH_SIZE,
                                  shuffle = True,
                                  num_workers = 6)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MyCNN(num_labels = 6).to(device)
    total_params = sum(p.numel() for p in model.parameters())
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    logger.info(f"Training in progress: {model.NETWORK_NAME}  |  Toltal parameter number: {total_params}")
    for epoch in range(NUM_EPOCHS):
        model.train()  # 设置为训练模式
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in dataloader_train:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        # 每个epoch结束后，打印训练集的损失和准确度
        epoch_loss = running_loss / len(dataloader_train)
        epoch_accuracy = 100 * correct / total
        

        # 验证集评估
        model.eval()  # 切换到评估模式
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in dataloader_valid:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        # 计算验证集的损失和准确度
        val_loss /= len(dataloader_valid)
        val_accuracy = 100 * val_correct / val_total
        logger.info("")
        logger.info(f"Epoch [{epoch+1}/{NUM_EPOCHS}]")
        logger.info(f"Train Loss: {epoch_loss:.4f}, Train Accuracy: {epoch_accuracy:.2f}%")
        logger.info(f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.2f}%")
        logger.info("")
    
    torch.save(model.state_dict(), MODEL_SAV_PATH)
    logger.info("Training Finished!")