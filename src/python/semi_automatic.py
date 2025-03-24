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
import matplotlib.pyplot as plt

PI = numpy.pi
LOG_SOURCE = "semi_automatic"
CAMERA_CENTER = 320

# 是初始化实验环境的时候了
LogUtils.log(LOG_SOURCE, "Initializing experiment environment...")
# 首先，以创建与 QLabs 的连接为目标吧
qlab = QLabsUtils.get_qlab("localhost")
# 赐予地板和墙壁吧
EnvironmentUtils.set_floor(qlab)
EnvironmentUtils.set_wall(qlab)
# 是创建 QBot 实体的时候了
# 也就是说需要确定位置和朝向
location = [0.0, 1.5, 0.1]
rotation = [0,0,0]
qbot = QBotUtils.get_qbot(qlab,location,rotation)
LogUtils.log(LOG_SOURCE, "Experiment environment initialized...")

# 前有 QBot 基础数值和分类器的设置，敬请见证
control_period = 0.05
controller = PIDController(qbot, control_period)

myCNN = MyCNN(6)
classifier = Classifier("src/resources/model_2025-03-22-184045.pth", myCNN)

# 设置 x 轴误差图像样式
fig, ax = plt.subplots()
ax.set_xlim(-50, 50)  # x轴范围
ax.set_ylim(-1, 1)  # x轴范围
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_position('center')
point, = ax.plot([], [], 'ro')
plt.ion()
plt.draw()
fig.canvas.manager.set_window_title("Monitor | Error on X-axis")
plt.show()

time.sleep(2)
LogUtils.log(LOG_SOURCE, "Program initiated, controlled by PID controller. Screenshot disabled. Control period: 0.05s.")
controller.start()
while True:
    is_success, image_raw = QBotUtils.get_image(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD)
    image = Image.fromarray(image_raw)
    if is_success:
        label = classifier.classify(image)
        # print(f"当前路径类型：{label}")
        
        # Monitor of Down Camera
        cv2.imshow("Monitor | Down Camera", image_raw)
        cv2.waitKey(10)
    match label:
        case "single":
            center = controller.get_center(image_raw)
            error = center - CAMERA_CENTER
            if 'text' in globals(): text.remove()
            point.set_data([error], [0])
            text = plt.text(
                error, 0.3,           # 坐标位置
                f"error = {error}", # 文本内容（保留1位小数）
                ha='center',            # 水平居中对齐
                va='bottom',            # 垂直底部对齐
                fontsize=12,
                color='red'
            )
            message = "Current error on X-axis: " + str(error)
            LogUtils.log(LOG_SOURCE, message)
            if abs(error) <= 200:
                control_variable = controller.compute(error)
                message = "Generated control variable: " + str(control_variable)
                LogUtils.log(LOG_SOURCE, message)
                controller.error_correction(control_variable)
        
        # 也就是说，接下来献上完全离开路径的可能，敬请见证
        case "off_track":
            controller.stop()
            LogUtils.log(LOG_SOURCE, "Track lost, program terminated!")
            QBotUtils.get_image_show(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD, "Finally Sent Image")
            cv2.waitKey(0)
            break
        
        # 是统一处理其他情况的时候了
        case _:
            controller.stop()
            message = "Track detected: " + label
            LogUtils.log(LOG_SOURCE, message)

            match label:
                case "t_left":
                    LogUtils.log(LOG_SOURCE, "Multi-track detected, please select a way manually. (a/w)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "Left way selected")
                            controller.simple_left()
                        case "w":
                            LogUtils.log(LOG_SOURCE, "Straight way selected")
                            controller.simple_straight()
                case "t_middle":
                    LogUtils.log(LOG_SOURCE, "Multi-track detected, please select a way manually. (a/d)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "Left way selected.")
                            controller.simple_left()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "Right way selected.")
                            controller.simple_right()
                case "t_right":
                    LogUtils.log(LOG_SOURCE, "Multi-track detected, please select a way manually. (w/d)")
                    signal = input()
                    match signal:
                        case "w":
                            LogUtils.log(LOG_SOURCE, "Straight way selected.")
                            controller.simple_straight()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "Right way selected.")
                            controller.simple_right()
                case "cross":
                    LogUtils.log(LOG_SOURCE, "Multi-track detected, please select a way manually. (a/w/d)")
                    signal = input()
                    match signal:
                        case "a":
                            LogUtils.log(LOG_SOURCE, "Left way selected.")
                            controller.simple_left()
                        case "w":
                            LogUtils.log(LOG_SOURCE, "Straight way selected.")
                            controller.simple_straight()
                        case "d":
                            LogUtils.log(LOG_SOURCE, "Right way selected.")
                            controller.simple_right()

            # controller.simple_straight()
            controller.start()

    # 程序退出万岁
    if keyboard.is_pressed("q"):
        wheel_speed_left = 0
        wheel_speed_right = 0
        qbot.command_and_request_state(wheel_speed_right, wheel_speed_left)
        LogUtils.log(LOG_SOURCE, "Program terminated manually...")
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