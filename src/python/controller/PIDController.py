from utils.LogUtils import LogUtils
from qvl.qbot_platform import QLabsQBotPlatform
from utils.QBotUtils import QBotUtils
import time
import cv2
from PIL import Image
import numpy as np

LOG_SOURCE = "PIDController"
BASE_SPEED = 0.1
MAX_SPEED = 0.5

class PIDController:
    def __init__(self, qbot, control_priod):
        
        self.Kp = 0.04
        self.Ki = 0.003
        self.Kd = 0.2
        self.prev_error = 0
        self.intergral = 0
        self.control_priod = control_priod
        
        
        self.qbot = qbot
        self.stop()
        LogUtils.log(LOG_SOURCE, "PID控制器已绑定 QBot 实例")

    def compute(self, error):
        self.intergral += error * self.control_priod
        derivative = (error - self.prev_error) / self.control_priod
        P = self.Kp * error
        I = self.Ki * self.intergral
        D = self.Kd * derivative
        output = P + I + D
        self.prev_error = error
        return output
    
    def get_center(self, image_raw):

        image_roi = image_raw[185:215,:]
        
        # cv2.imshow("sss", image_roi)
        # cv2.waitKey(0)

        # 二值化处理（假设路径为高亮度）
        _, thresh = cv2.threshold(image_roi, 200, 255, cv2.THRESH_BINARY)

        # 计算非零像素坐标
        nonzero = np.argwhere(thresh)

        # 计算横向中心坐标
        center = np.mean(nonzero[:, 1]).astype(int)
        
        return center
    
    
    def error_correction(self, control_variable):
        
        if self.wheel_speed_left < MAX_SPEED and self.wheel_speed_right < MAX_SPEED:
            self.wheel_speed_left += control_variable / 1000
            self.wheel_speed_right -= control_variable / 1000
            
        self.apply_speed()
    
    def stop(self):
        self.wheel_speed_left = self.wheel_speed_right = 0
        self.apply_speed()
        
    def start(self):
        self.wheel_speed_right = self.wheel_speed_left = BASE_SPEED
        self.apply_speed()
    
    def apply_speed(self):
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
    
    def simple_left(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（左）")
        self.wheel_speed_left = -0.05
        self.wheel_speed_right = 0.07
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(1)
        self.stop()
        LogUtils.log(LOG_SOURCE, "自动转向（左）完成")

        
    def simple_right(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（右）")
        self.wheel_speed_left = 0.07
        self.wheel_speed_right = -0.05
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(1)
        LogUtils.log(LOG_SOURCE, "自动转向（右）完成")
        
    def simple_straight(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（直行）")
        self.start()
        time.sleep(1)
        self.stop()
        LogUtils.log(LOG_SOURCE, "自动转向（直行）完成")