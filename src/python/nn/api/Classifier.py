from nn.dataset import LabelMapper
import torch
from nn.dataset.Preprocessing import Preprocessing
from nn.dataset.LabelMapper import LabelMapper

class Classifier:
    def __init__(self, model_path, network):
        self.model_path = model_path
        self.network = network
        self.model = network()
        self.model.load_state_dict(torch.load(self.model_path))
        self.model.eval()
    
    def classify(self,image):
        image = Preprocessing.transform_0(image)
        image = image.unsqueeze(0)  # 增加批次维度
        
        # 进行推理
        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
            category = predicted.item()

        predict = LabelMapper.cat_to_label[category]
        return predict