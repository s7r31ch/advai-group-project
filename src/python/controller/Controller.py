class Controller:
    def __init__(self, qbot, control_period):
        self.qbot = qbot
        self.control_period = control_period
        
    def stop(self):
        self.wheel_speed_left = self.wheel_speed_right = 0
        self.apply_speed()
        
    def apply_speed(self):
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)