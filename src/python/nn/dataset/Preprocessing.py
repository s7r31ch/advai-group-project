import torchvision.transforms as transforms

class Preprocessing:
    # 定义图像预处理操作
    transform_0 = transforms.Compose([
        # 这里假设图片尺寸已经是640x400，如果需要调整，请修改此处
        transforms.Resize((400, 640)),
        transforms.ToTensor(),  # 将图像转换为Tensor，并归一化到[0,1]
        transforms.Normalize((0.5,), (0.5,))  # 对灰度图进行归一化（均值0.5，标准差0.5）
    ])