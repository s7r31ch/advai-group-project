from devtoolkit.Log4P import Log4P

class KeyboardController:
    
    CONTROL_DELTA = 0.05
    
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
    
    def send(self, signal):
        match signal:
            case "w":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                self.logger.info("Accelerate")
            case "s":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                self.logger.info("Decelerate")
            case "a":
                self.wheel_speed_left -= self.delta
                self.wheel_speed_right += self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                self.logger.info("Yaw to left")
            case "d":
                self.wheel_speed_left += self.delta
                self.wheel_speed_right -= self.delta
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                self.logger.info("Yaw to right")
            case "b":
                self.wheel_speed_left = 0
                self.wheel_speed_right = 0
                self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)
                self.logger.info("Stop")