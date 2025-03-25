from devtoolkit.Log4P import Log4P
import time
import cv2
import numpy as np

from controller.BaseController import BaseController
from devtoolkit.Log4P import Log4P



class PIDController(BaseController):
    
    BASE_SPEED = 0.1
    MAX_SPEED = 0.5
    
    def __init__(self, qbot, control_period):
        self.logger = Log4P(enable_level = True,
                      enable_timestamp = True,
                      enable_source = True,
                      source = "PIDController")
        super().__init__(qbot, control_period)
        self.logger.info("PID controller binded to QBot Instance.")
        
        self.Kp = 0.040
        self.Ki = 0.001
        self.Kd = 0.065
        self.prev_error = 0
        self.intergral = 0
        
        self.stop()
     
    def compute(self, error):
        self.intergral += error * self.control_priod
        derivative = (error - self.prev_error) / self.control_priod
        P = self.Kp * error
        I = self.Ki * self.intergral
        D = self.Kd * derivative
        output = P + I + D
        self.prev_error = error
        return output
    
    # 以获取白线中心为目标吧
    def get_center(self, image_raw):

        # 很可能是对 ROI 区域的获取
        image_roi = image_raw[185:215,:]
        
        _, thresh = cv2.threshold(image_roi, 200, 255, cv2.THRESH_BINARY)
        nonzero = np.argwhere(thresh)
        center = np.mean(nonzero[:, 1]).astype(int)
        
        return center
    
    # 很可能是对误差的修正，也就是说输入控制量，控制左右轮差速，无返回值
    def error_correction(self, control_variable):
        
        # 献上对速度的控制，基于控制量
        self.set_speed(wheel_speed_left = self.wheel_speed_left + control_variable / 1000,
                       wheel_speed_right = self.wheel_speed_right - control_variable / 1000,
                       speed_constraint = self.MAX_SPEED).apply_speed()
    
    # 仅 PID 控制器有，让机器以 BASE_SPEED 运行起来
    def start(self):
        self.set_speed(wheel_speed_left = self.BASE_SPEED,
                       wheel_speed_right = self.BASE_SPEED).apply_speed()
    
    # 前有开环控制转向的预感，敬请见证！
    # simple_left()
    # simple_right()
    # simple_straight()
    def simple_left(self):
        self.logger.info("Steering to left automatically...")
        self.wheel_speed_left = -0.05
        self.wheel_speed_right = 0.07
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(0.5)
        self.logger.info("Left steering completed.")

    def simple_right(self):
        self.logger.info("Steering to right automatically...")
        self.wheel_speed_left = 0.07
        self.wheel_speed_right = -0.05
        self.apply_speed()
        time.sleep(5)
        self.start()
        time.sleep(0.5)
        self.logger.info("Right steering completed.")
        
    def simple_straight(self):
        self.logger.info("Going straight automatically...")
        self.start()
        time.sleep(0.5)
        self.logger.info("Continue to main program.")