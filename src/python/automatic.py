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

PI = numpy.pi
LOG_SOURCE = "main"

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

wheel_speed_left = 0
wheel_speed_right = 0
delta = 0.05


while True:
    qbot.command_and_request_state(wheel_speed_right, wheel_speed_left)
    if keyboard.is_pressed("w"):
        wheel_speed_left += delta
        wheel_speed_right += delta
        LogUtils.log(LOG_SOURCE, "加速")
        
    if keyboard.is_pressed("s"):
        wheel_speed_left -= delta
        wheel_speed_right -= delta
        LogUtils.log(LOG_SOURCE, "减速")
        
    if keyboard.is_pressed("a"):
        wheel_speed_left -= delta
        wheel_speed_right += delta
        LogUtils.log(LOG_SOURCE, "前向左偏航/后向右偏航")
        
    if keyboard.is_pressed("d"):
        wheel_speed_left += delta
        wheel_speed_right -= delta
        LogUtils.log(LOG_SOURCE, "前向右偏航/后向左偏航")
    
    if keyboard.is_pressed("b"):
        wheel_speed_left = 0
        wheel_speed_right = 0
        LogUtils.log(LOG_SOURCE, "停止")
    
    # 居然是退出
    if keyboard.is_pressed("q"):
        wheel_speed_left = 0
        wheel_speed_right = 0
        qbot.command_and_request_state(wheel_speed_right, wheel_speed_left)
        LogUtils.log(LOG_SOURCE, "检测到 'Q/q' 键，退出程序！")
        break
    
    time.sleep(0.1)
















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