from PIL import Image
from nn.api.Classifier import Classifier
from nn.network.MyCNN import MyCNN

# 加载并预处理图像
image_path = "src/resources/ds_test/straight Image.png"
image = Image.open(image_path).convert('L')  # 灰度图

classifier = Classifier("src/resources/model_2025-03-22-171952.pth", MyCNN)

print(f"预测类型为：{classifier.classify(image)}")
