from utils.LogUtils import LogUtils

LOG_SOURCE = "KeyboardController"

class KeyboardController:
    
    def __init__(self, qbot, delta):
        self.wheel_speed_left = 0
        self.wheel_speed_right = 0
        self.delta = delta
        self.qbot = qbot
        LogUtils.log(LOG_SOURCE, "键盘控制器已绑定 QBot 实例")
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
    
    def send(self, signal):
        match signal:
            case "w":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "加速")
            case "s":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "减速")
            case "a":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "前向左偏航/后向右偏航")
            case "d":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "前向右偏航/后向左偏航")
            case "b":
                self.wheel_speed_left = 0
                self.wheel_speed_right = 0
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                LogUtils.log(LOG_SOURCE, "停止")