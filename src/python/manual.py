import numpy
import time
import cv2
import keyboard

from utils.QLabsUtils import QLabsUtils
from utils.EnvironmentUtils import EnvironmentUtils
from utils.QBotUtils import QBotUtils
from qvl.qbot_platform import QLabsQBotPlatform
from controller.KeyboardController import KeyboardController
from utils.LogUtils import LogUtils

PI = numpy.pi
LOG_SOURCE = "manual"

# 是初始化实验环境的时候了
LogUtils.log(LOG_SOURCE, "Initializing experiment environment...")
# 首先，以创建与 QLabs 的连接为目标吧
qlab = QLabsUtils.get_qlab("localhost")
# 赐予地板和墙壁吧
EnvironmentUtils.set_floor(qlab)
EnvironmentUtils.set_wall(qlab)
# 是创建 QBot 实体的时候了
# 也就是说需要确定位置和朝向
location = [-1.5, 0, 0.1]
rotation = [0,0,PI/2]
qbot = QBotUtils.get_qbot(qlab,location,rotation)
LogUtils.log(LOG_SOURCE, "Experiment environment initialized...")

# 前面需要设置QBot初始状态以及控制信号的增量
# 献上键盘控制器与 QBot 实例的绑定吧
delta = 0.05
controller = KeyboardController(qbot, delta)

# 接下来，设置键盘选项很有用
def press(event):
    key = event.name.lower()
    controller.send(key)
def block_input(event):
    if event.event_type == 'down': 
        return False
keyboard.on_press(press)
keyboard.hook(block_input)

# 前有主循环，敬请见证
# 前面需要设置下视摄像头截图保存路径，暂且以 0.5s 的间隔截图吧
image_sav_path = "src/resources/record_downcam/"
is_record = 0
LogUtils.log(LOG_SOURCE, "Program initiated, controlled by keboard. Screenshot enabled. Control period: 0.1s.")
input("Press any key to start")
try:
    while True:
        # 是自动截图的时候了
        is_record = (is_record + 1) % 10
        if is_record == 0:
            is_success, image = QBotUtils.get_image(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD)
            timestamp = str(LogUtils.get_current_timestamp())
            file_name = image_sav_path + timestamp + ".jpg"
            cv2.imwrite(file_name, image)
            LogUtils.log(LOG_SOURCE,"Screenshot captured")
            
        # 居然是退出
        if keyboard.is_pressed("q"):
            wheel_speed_left = 0
            wheel_speed_right = 0
            qbot.command_and_request_state(wheel_speed_right, wheel_speed_left)
            LogUtils.log(LOG_SOURCE, "Program terminated manually...")
            break
        time.sleep(0.1)
except Exception as e:
    LogUtils.log(LOG_SOURCE, e)

