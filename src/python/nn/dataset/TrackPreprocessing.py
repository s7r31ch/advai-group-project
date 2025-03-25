from torchvision import transforms

class TrackPreprocessing:
    # 图像预处理变换
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # 调整图像大小
        transforms.ToTensor(),           # 转换为张量
        transforms.Normalize((0.5,), (0.5,))  # 标准化
    ])