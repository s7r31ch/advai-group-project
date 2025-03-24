from utils.LogUtils import LogUtils
import time
import cv2
import numpy as np

LOG_SOURCE = "PIDController"
BASE_SPEED = 0.1
MAX_SPEED = 0.5

class PIDController:
    def __init__(self, qbot, control_priod):
        
        self.Kp = 0.035
        self.Ki = 0.002
        self.Kd = 0.045
        self.prev_error = 0
        self.intergral = 0
        self.control_priod = control_priod
        
        
        self.qbot = qbot
        self.stop()
        LogUtils.log(LOG_SOURCE, "PID controller binded to QBot Instance.")

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
        LogUtils.log(LOG_SOURCE, "Steering to left automatically...")
        self.wheel_speed_left = -0.05
        self.wheel_speed_right = 0.07
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(0.5)
        # self.stop()
        LogUtils.log(LOG_SOURCE, "Left steering completed.")

        
    def simple_right(self):
        LogUtils.log(LOG_SOURCE, "Steering to right automatically...")
        self.wheel_speed_left = 0.07
        self.wheel_speed_right = -0.05
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(0.5)
        # self.stop()
        LogUtils.log(LOG_SOURCE, "Right steering completed.")
        
    def simple_straight(self):
        LogUtils.log(LOG_SOURCE, "Going straight automatically...")
        self.start()
        time.sleep(0.5)
        # self.stop()
        LogUtils.log(LOG_SOURCE, "Continue to main program.")