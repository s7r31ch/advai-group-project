import numpy
import time
import cv2
from qvl.qbot_platform import QLabsQBotPlatform
from utils.LogUtils import LogUtils

PI = numpy.pi
LOG_SOURCE = "QBotUtils"

class QBotUtils:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_qbot(qlab, location, rotation):
        LogUtils.log(LOG_SOURCE, "Generating QBot instance...")
        qlabs_qbot_platform = QLabsQBotPlatform(qlab)
        qlabs_qbot_platform.spawn_id(0, location, rotation, scale=[1,1,1], configuration=1, waitForConfirmation= False)
        time.sleep(0.5)
        LogUtils.log(LOG_SOURCE, "QBot instance generated.")
        return qlabs_qbot_platform
    
    @staticmethod
    def get_image(qbot, camera_type):
        is_success, image = qbot.get_image(camera_type)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return (is_success, image)

    @staticmethod
    def get_image_show(qbot, camera_type, title="NOW"):
        is_success, image = qbot.get_image(camera_type)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        cv2.imshow(title, image)
