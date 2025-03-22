from datetime import datetime

LOG_SOURCE = "LogUtils"

class LogUtils:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_current_readable_timestamp(regex):
        timestamp = datetime.now()
        timestamp_formatted = timestamp.strftime(regex)
        return timestamp_formatted
    
    @staticmethod
    def get_current_timestamp():
        timestamp = datetime.now()
        timetamp_formatted = int(timestamp.timestamp() * 1000)
        return timetamp_formatted
    
    @staticmethod
    def log(source, message):
        regex = "%Y-%m-%d %H:%M:%S"
        print(f"[{LogUtils.get_current_readable_timestamp(regex)}] {source}: {message}")
        
    @staticmethod
    def get_model_name_timestamp():
        regex = "%Y-%m-%d-%H%M%S"
        return datetime.now().strftime(regex)