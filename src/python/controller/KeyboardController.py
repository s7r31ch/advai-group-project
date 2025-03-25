from devtoolkit.Log4P import Log4P
from controller.BaseController import BaseController

class KeyboardController(BaseController):
    
    CONTROL_DELTA = 0.05
    SPEED_MAX = 1
    
    def __init__(self, 
                 qbot, 
                 control_period):
        self.logger = Log4P(enable_level = True,
                       enable_timestamp = True,
                       enable_source = True,
                       source = "KeyboardController")
        
        super().__init__(qbot, control_period)
        self.logger.info("Keyboard controller binded to QBot Instance.")
        
        
        self.logger.info("Keyboard controller binded to QBot Instance.")
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
        
    def initialize(self):
        self.stop()
    
    def send(self, signal):
        match signal:
            case "w":
                self.set_speed(wheel_speed_left = self.wheel_speed_left + self.CONTROL_DELTA,
                               wheel_speed_right = self.wheel_speed_right + self.CONTROL_DELTA).apply_speed()
                self.logger.info("Accelerate")
            case "s":
                self.set_speed(wheel_speed_left = self.wheel_speed_left - self.CONTROL_DELTA,
                               wheel_speed_right = self.wheel_speed_right - self.CONTROL_DELTA).apply_speed()
                self.logger.info("Decelerate")
            case "a":
                self.set_speed(wheel_speed_left = self.wheel_speed_left - self.CONTROL_DELTA,
                               wheel_speed_right = self.wheel_speed_right + self.CONTROL_DELTA).apply_speed()
                self.logger.info("Yaw to left")
            case "d":
                self.set_speed(wheel_speed_left = self.wheel_speed_left + self.CONTROL_DELTA,
                               wheel_speed_right = self.wheel_speed_right - self.CONTROL_DELTA).apply_speed()
                self.logger.info("Yaw to right")
            case "b":
                self.stop()
                self.logger.info("Stop")