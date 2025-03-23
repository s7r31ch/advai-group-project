from utils.LogUtils import LogUtils

LOG_SOURCE = "KeyboardController"

class KeyboardController:
    
    def __init__(self, qbot, delta):
        self.wheel_speed_left = 0
        self.wheel_speed_right = 0
        self.delta = delta
        self.qbot = qbot
        LogUtils.log(LOG_SOURCE, "Keyboard controller binded to QBot Instance.")
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
    
    def send(self, signal):
        match signal:
            case "w":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "Accelerate")
            case "s":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "Decelerate")
            case "a":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "Yaw to left")
            case "d":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "Yaw to right")
            case "b":
                self.wheel_speed_left = 0
                self.wheel_speed_right = 0
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "Stop")