import torch
from torch.utils.data import DataLoader

from utils.DatasetUtils import DatasetUtils
from nn.dataset.TrackDataset import TrackDataset
from nn.dataset.TrackPreprocessing import TrackPreprocessing

if __name__ == "__main__":
    
    # 有重要参数设置的预感，敬请见证
    LABEL_FILE_PATH = "src/resources/label.csv"
    DATASET_DIR = "src/resources/ds_train"
    BATCH_SIZE = 32
    
    dataframe = DatasetUtils.get_dataframe(label_file_path = LABEL_FILE_PATH,
                                           dataset_dir = DATASET_DIR)
    
    dataset = TrackDataset(dataframe = dataframe,
                                 transform = TrackPreprocessing.transform)
    
    train_size = int(0.8*len(dataset))
    valid_size = len(dataset) - train_size
    
    dataset_train, dataset_test = torch.utils.data.random_split(dataset, [train_size, valid_size])
    
    dataloader_train = DataLoader(dataset = dataset_train,
                                  batch_size = BATCH_SIZE,
                                  shuffle = True,
                                  num_workers = 6)
    
    dataloader_valid = DataLoader(dataset = dataset_test,
                                  batch_size = BATCH_SIZE,
                                  shuffle = True,
                                  num_workers = 6)