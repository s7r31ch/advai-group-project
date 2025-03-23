from PIL import Image
from nn.api.Classifier import Classifier
from nn.network.MyCNN import MyCNN

# 有加载模型的预感
myCNN = MyCNN(6)
classifier = Classifier("src/resources/model_2025-03-22-184045.pth", myCNN)

# 加载并预处理图像
image_path = "src/resources/ds_test/22.86_Corner.png"
image = Image.open(image_path).convert('L')  # 灰度图

print(f"predicted type: {classifier.classify(image)}")
