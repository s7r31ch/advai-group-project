import numpy
import time
import cv2
import keyboard

from utils.QLabsUtils import QLabsUtils
from utils.EnvironmentUtils import EnvironmentUtils
from utils.QBotUtils import QBotUtils
from qvl.qbot_platform import QLabsQBotPlatform
from controller.PIDController import PIDController
from utils.LogUtils import LogUtils
from nn.api.Classifier import Classifier
from nn.network.MyCNN import MyCNN
from PIL import Image

PI = numpy.pi
LOG_SOURCE = "automatic"

# 是初始化实验环境的时候了
LogUtils.log(LOG_SOURCE, "正在初始化实验环境...")
# 首先，以创建与 QLabs 的连接为目标吧
qlab = QLabsUtils.get_qlab("localhost")
# 赐予地板和墙壁吧
EnvironmentUtils.set_floor(qlab)
EnvironmentUtils.set_wall(qlab)
# 是创建 QBot 实体的时候了
# 也就是说需要确定位置和朝向
location = [-1.5, 0, 0.1]
rotation = [0,0,-PI/2]
qbot = QBotUtils.get_qbot(qlab,location,rotation)
LogUtils.log(LOG_SOURCE, "实验环境初始化完成...")

# 前有 QBot 基础数值和分类器的设置，敬请见证
control_period = 0.1
controller = PIDController(qbot, control_period)

myCNN = MyCNN(6)
classifier = Classifier("src/resources/model_2025-03-22-184045.pth", myCNN)

time.sleep(2)

while True:
    is_success, image_raw = QBotUtils.get_image(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD)
    image = Image.fromarray(image_raw)
    if is_success:
        label = classifier.classify(image)
        # print(f"当前路径类型：{label}")
        
    match label:
        case "single":
            controller.set_speed(0.07).apply_speed()
        
        # 也就是说，接下来献上完全离开路径的可能，敬请见证
        case "off_track":
            controller.stop()
            LogUtils.log(LOG_SOURCE, "目标失去路径跟踪，程序中断！")
            QBotUtils.get_image_show(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD, "最后回传图像")
            cv2.waitKey(0)
            break
        
        # 是统一处理其他情况的时候了
        case _:
            controller.stop()
            message = "检测到路径类型：" + label
            LogUtils.log(LOG_SOURCE, message)
            
            match label:
                case "t_left":
                    LogUtils.log(LOG_SOURCE, "检测到多路径，需要手动选择(a/w)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "已选择左转")
                            controller.simple_left()
                        case "w":
                            LogUtils.log(LOG_SOURCE, "已选择直行")
                            controller.simple_straight()
                case "t_middle":
                    LogUtils.log(LOG_SOURCE, "检测到多路径，需要手动选择(a/d)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "已选择左转")
                            controller.simple_left()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "已选择右转")
                            controller.simple_right()
                case "t_right":
                    LogUtils.log(LOG_SOURCE, "检测到多路径，需要手动选择(w/d)")
                    signal = input()
                    match signal:
                        case "w":
                            LogUtils.log(LOG_SOURCE, "已选择直行")
                            controller.simple_straight()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "已选择右转")
                            controller.simple_right()
                case "cross":
                    LogUtils.log(LOG_SOURCE, "检测到多路径，需要手动选择(a/w/d)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "已选择左转")
                            controller.simple_left()
                        case "w":
                            LogUtils.log(LOG_SOURCE, "已选择直行")
                            controller.simple_straight()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "已选择右转")
                            controller.simple_right()
    
    # 程序退出万岁
    if keyboard.is_pressed("q"):
        wheel_speed_left = 0
        wheel_speed_right = 0
        qbot.command_and_request_state(wheel_speed_right, wheel_speed_left)
        LogUtils.log(LOG_SOURCE, "检测到 'q' 键，退出程序！")
        break        
    
    time.sleep(control_period)
















# # 前方有测试图像获取的预感
# # QLabsQBotPlatform.CAMERA_RGB
# # QLabsQBotPlatform.CAMERA_DOWNWARD
# is_success, image = QBotUtils.get_image(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD)
# if is_success:
#     cv2.imshow("test",image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# # 前方有测试 QBot 实例移动的预感
# qbot.command_and_request_state(0.5,0.5)
# time.sleep(2)
# qbot.command_and_request_state(0.5,0)
# time.sleep(2)
# qbot.command_and_request_state(0,0)

# # 如果有 PID 控制器的话
# # 分别赐予比例项、积分项和微分项吧
# # 接下来，调整 Kp, Ki, Kd 很有用
# Kp = 1
# Ki = 1
# Kd = 1
# pid_controller = PIDController(Kp, Ki, Kd)