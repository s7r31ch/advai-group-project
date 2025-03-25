import pandas as pd
import os

class DatasetUtils:
    
    @staticmethod
    def get_dataframe(label_file_path,
                      dataset_dir):
        dataframe = pd.read_csv(filepath_or_buffer = label_file_path,
                                header = None,
                                names = ["sample_path", "label"])
        dataframe["sample_path"] = dataframe["sample_path"].apply(lambda name:os.path.join(dataset_dir,name))
        return dataframe