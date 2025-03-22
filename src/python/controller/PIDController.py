from utils.LogUtils import LogUtils
from qvl.qbot_platform import QLabsQBotPlatform
from utils.QBotUtils import QBotUtils
import time
import cv2

LOG_SOURCE = "PIDController"

class PIDController:
    def __init__(self, qbot, control_priod):
        self.qbot = qbot
        self.stop()
        self.Kp = 1
        self.Ki = 1
        self.Kd = 1
        self.prev_error = 0
        self.control_priod = control_priod
        self.wheel_speed_right = self.wheel_speed_left = 0
        LogUtils.log(LOG_SOURCE, "PID控制器已绑定 QBot 实例")

    def compute(self, error, dt):
        self.control_priod += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.Kp * error + self.Ki * self.control_priod + self.Kd * derivative
        self.prev_error = error
        return output
    
    def stop(self):
        self.wheel_speed_left = self.wheel_speed_right = 0
        self.apply_speed()
        
    def set_speed(self, speed):
        self.wheel_speed_right = self.wheel_speed_left = speed
        return self
    
    def apply_speed(self):
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
        return self
    
    def simple_left(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（左）")
        self.wheel_speed_left = -0.05
        self.wheel_speed_right = 0.07
        self.apply_speed()
        time.sleep(5)
        self.stop()
        self.set_speed(0.07).apply_speed()
        time.sleep(2)
        self.stop()
        LogUtils.log(LOG_SOURCE, "自动转向（左）完成")

        
    def simple_right(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（右）")
        self.wheel_speed_left = 0.07
        self.wheel_speed_right = -0.05
        self.apply_speed()
        time.sleep(5)
        self.stop()
        self.set_speed(0.07).apply_speed()
        time.sleep(2)
        LogUtils.log(LOG_SOURCE, "自动转向（右）完成")
        
    def simple_straight(self):
        LogUtils.log(LOG_SOURCE, "正在进行自动转向（直行）")
        self.set_speed(0.07).apply_speed()
        time.sleep(2)
        LogUtils.log(LOG_SOURCE, "自动转向（直行）完成")