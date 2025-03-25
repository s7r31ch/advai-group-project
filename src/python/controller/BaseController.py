class BaseController:
    # 绑定控制器
    # 设置控制间隔
    # 停止机器人实例
    def __init__(self, qbot, control_period):
        self.qbot = qbot
        self.control_period = control_period
        self.stop()
    
    # 子类需要重写此方法
    # 指定切换到此控制器时的初始动作
    def initialize(self):
        pass
        
    def set_speed(self,
                  wheel_speed_left,
                  wheel_speed_right,
                  **kwargs):
        # 要是存在速度限制的话
        if "speed_constraint" not in kwargs or abs(wheel_speed_left) <= kwargs["speed_constraint"] and abs(wheel_speed_right) <= kwargs["speed_constraint"]:
            self.wheel_speed_left = wheel_speed_left
            self.wheel_speed_right = wheel_speed_right
            
        # 你有资格啊，正因为你有资格。链式编程，敬请见证！
        return self

    def stop(self):
        self.set_speed(wheel_speed_left = 0,
                       wheel_speed_right = 0)
        self.apply_speed()
        
    def apply_speed(self):
        self.qbot.command_and_request_state(self.wheel_speed_right, self.wheel_speed_left)