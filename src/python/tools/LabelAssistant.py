import os
import cv2
import csv

from utils.LogUtils import LogUtils

LOG_SOURCE = "LabelAssistant"

class LabelAssistant:
    
    def __init__(self, dataset_path, category_file_path):
        self.dataset_path = dataset_path
        self.category_file_path = category_file_path
    
    @staticmethod
    def fit(key):
        match (key & 0xFF):
            case 97: record = "t_left"
            case 100: record = "t_right"
            case 115: record = "t_middle"
            case 119: record = "single"
            case 120: record = "cross"
            case 112:
                LogUtils.log(LOG_SOURCE, "Delete this picture? (y,N)")
                yN = input()
                if yN.lower() == "y": 
                    record = "delete"
                else:
                    record = LabelAssistant.fit(key)
        return record
    
    def start(self):
        
        if os.path.exists(self.category_file_path):
            LogUtils.log(LOG_SOURCE, "Label file already exist, overwrite it? (y,N)")
            yN = input()
            if yN.lower() != "y": 
                LogUtils.log(LOG_SOURCE, "User discards label file, program terminated")
                os._exit(0)
        
        category_file = open(self.category_file_path, "w", newline="")
        
        for image_name in os.listdir(self.dataset_path):
            image_path_name = self.dataset_path + "/" + image_name
            image = cv2.imread(image_path_name)
            cv2.imshow(image_name, image[100:300,:])
            key = cv2.waitKey(0)
            category = LabelAssistant.fit(key)
            if category == "delete":
                os.remove(image_path_name)
                message = "Picture deleted:" + image_name
            else:
                record = (image_name, category)
                csv.writer(category_file).writerow(record)
                category_file.flush()
                message = "Label recorded: Picture" + image_name + " labeled " + category
                
            LogUtils.log(LOG_SOURCE, message)
            cv2.destroyWindow(image_name)
            