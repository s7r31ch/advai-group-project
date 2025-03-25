import threading
from PIL import Image
from qvl.qbot_platform import QLabsQBotPlatform
import cv2
import time
import keyboard
import sys
import matplotlib.pyplot as plt
import os

from utils.QLabsUtils import QLabsUtils
from utils.EnvironmentUtils import EnvironmentUtils
from utils.QBotUtils import QBotUtils
from devtoolkit.Log4P import Log4P
from devtoolkit.KeyboardMonitor import KeyboardMonitor
from controller.KeyboardController import KeyboardController
from controller.PIDController import PIDController
from nn.network.MyCNN import MyCNN
from nn.api.Classifier import Classifier

def change_control_type():
    global control_type, control_type_history, controller, command_sequence, plt, fig
    control_type = input("Select a control method: (m/a/p)\n")
    control_type_history = False
    match control_type:
        case "m":
            fig.canvas.manager.window.hide()
            controller = keyboard_controller
            logger.info("Manual control selected.")
        case "a":
            fig.canvas.manager.window.show()
            controller = pid_controller
            logger.info("Auto control selected.")
        case "p":
            fig.canvas.manager.window.show()
            controller = pid_controller
            logger.info("Programmed control selected.")
            command_sequence = iter(input("Command sequences: "))
    
if __name__ == "__main__":
    
    # Parameters check before run
    IMAGE_SAV_DIR = "src/resources/saved-images"
    IMAGE_MODE = False
    CNN_MODEL_PATH = "src/resources/model_2025-03-22-184045.pth"
    
    # Parameters do not change
    _MANUAL_CONTROL_PERIOD = 0.1
    _PID_CONTROL_PERIOD = 0.05
    _CAMERA_CENTER = 320
    
    # Foundamental components setting
    logger = Log4P(enable_level = True,
               enable_timestamp = True,
               enable_source = True,
               source = "main(combination)")
    keyboard_monitor = KeyboardMonitor().start()
    keyboard_monitor.daemon = threading.Thread(target = keyboard_monitor.listen_daemon,
                                               daemon = True)
    keyboard_monitor.daemon.start()
    
    # Experimental environment setting
    logger.info("Initializing experimental environment...")
    qlab = QLabsUtils.get_qlab("localhost")
    EnvironmentUtils.set_floor(qlab)
    EnvironmentUtils.set_wall(qlab)
    location = [0.0, 1.5, 0.1]
    rotation = [0,0,0]
    qbot = QBotUtils.get_qbot(qlab,location,rotation)
    logger.info("Experiment environment initialized.")
    
    # Controller initializing
    keyboard_controller = KeyboardController(qbot = qbot,
                                             control_period = _MANUAL_CONTROL_PERIOD)
    pid_controller = PIDController(qbot = qbot,
                                   control_period = _PID_CONTROL_PERIOD)
    
    # CNN model loading
    myCNN = MyCNN(6)
    classifier = Classifier(CNN_MODEL_PATH, myCNN)
    logger.info("CNN model loaded.")
    
    # Visualization Initializing
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(-100, 100)  # x轴范围
    ax.set_ylim(-1, 1)  # x轴范围
    ax.yaxis.set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position('center')
    point, = ax.plot([], [], 'ro')
    fig.canvas.manager.set_window_title("Monitor | Error on X-axis")
    fig.canvas.manager.window.hide()
    
    # 初始关闭图像采集模式
    os.makedirs(IMAGE_SAV_DIR, exist_ok=True)
    
    # 也就是说，前方有对控制方式的选择
    change_control_type()
    
    # 主控制循环万岁
    while True:
        
        if not control_type_history: 
            controller.initialize()
            control_type_history = True
        
        # 献上对键盘实时输入的响应
        if keyboard.is_pressed("q"):
            logger.info("Program terminated to change control type.")
            controller.stop()
            change_control_type()
        
        if keyboard.is_pressed("g"):
            IMAGE_MODE = not IMAGE_MODE
            if IMAGE_MODE: logger.info("Image mode enabled.")
            else: logger.info("Image mod disabled.")
            
        if keyboard.is_pressed("esc"):
            logger.info("Program terminated manually.")
            controller.stop()
            sys.exit(0)
        
        # Monitor of Down Camera   
        is_success, image_raw = QBotUtils.get_image(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD)
        cv2.imshow("Monitor | Down Camera", image_raw)
        cv2.waitKey(10)
        if IMAGE_MODE:
            image_name = int(time.time())
            image_ext = ".jpg"
            image_path = f"{IMAGE_SAV_DIR}/{image_name}{image_ext}"
            cv2.imwrite(image_path, image_raw)
        
        # 前有手动控制
        if control_type == "m":
            key = keyboard_monitor.listen()
            if key is not None: controller.send(key)
            
        # 前有自动控制(包括半自动控制和预编程)
        elif control_type in {"a", "p"}:
            image = Image.fromarray(image_raw)
            label = classifier.classify(image)
            match label:
                case "single":
                    track_center = controller.get_track_center(image_raw)
                    error = track_center - _CAMERA_CENTER
                    message = "Current error on X-axis: " + str(error)
                    logger.info(message)
                    
                    # 献上对于过度误差的舍弃
                    if abs(error) <= 200:
                        message = "Current error on X-axis: " + str(error)
                        logger.info(message)
                        control_variable = controller.compute(error)
                        message = "Generated control variable: " + str(control_variable)
                        logger.info(message)
                        controller.error_correction(control_variable)
                        
                        if 'plt_text' in globals(): plt_text.remove()
                        point.set_data([error], [0])
                        plt_text = plt.text(
                            error, 0.3,           # 坐标位置
                            f"error = {error}", # 文本内容（保留1位小数）
                            ha='center',            # 水平居中对齐
                            va='bottom',            # 垂直底部对齐
                            fontsize=12,
                            color='red'
                        )
                        
                # 也就是说，接下来献上完全离开路径的可能，敬请见证
                case "off_track":
                    controller.stop()
                    logger.info("Track lost, program terminated!")
                    QBotUtils.get_image_show(qbot, QLabsQBotPlatform.CAMERA_DOWNWARD, "Finally Sent Image")
                    cv2.waitKey(0)
                    break
                
                # 是统一处理其他情况的时候了
                case _:
                    # 首先，先停下吧
                    controller.stop()
                    message = "Track detected: " + label
                    logger.info(message)
                    if control_type == "p":
                        signal = next(command_sequence, None)
                        if signal is None:
                            logger.info("Command sequence execution complete, please press c to contimue or press q to change control type.")
                            key = keyboard_monitor.wait_for("c", "q")
                            if key == "c":
                                command_sequence = iter(input("Command sequences: "))
                                continue
                            else:
                                change_control_type()
                                continue
                    match label:
                        case "t_left":
                            logger.info("Multi-track detected, please select a way manually. (a/w)")
                            if control_type == "a": signal = keyboard_monitor.wait_for("a","w")
                            match signal:
                                case "a":
                                    logger.info("Left way selected")
                                    controller.simple_left()
                                case "w":
                                    logger.info("Straight way selected")
                                    controller.simple_straight()
                        case "t_middle":
                            logger.info("Multi-track detected, please select a way manually. (a/d)")
                            if control_type == "a": signal = keyboard_monitor.wait_for("a","d")
                            match signal:
                                case "a":
                                    logger.info("Left way selected.")
                                    controller.simple_left()
                                case "d":
                                    logger.info("Right way selected.")
                                    controller.simple_right()
                        case "t_right":
                            logger.info("Multi-track detected, please select a way manually. (w/d)")
                            if control_type == "a": signal = keyboard_monitor.wait_for("w","d")
                            match signal:
                                case "w":
                                    logger.info("Straight way selected.")
                                    controller.simple_straight()
                                case "d":
                                    logger.info("Right way selected.")
                                    controller.simple_right()
                        case "cross":
                            logger.info("Multi-track detected, please select a way manually. (a/w/d)")
                            if control_type == "a": signal = keyboard_monitor.wait_for("a","w", "d")
                            match signal:
                                case "a":
                                    logger.info("Left way selected.")
                                    controller.simple_left()
                                case "w":
                                    logger.info("Straight way selected.")
                                    controller.simple_straight()
                                case "d":
                                    logger.info("Right way selected.")
                                    controller.simple_right()
                                    
        time.sleep(controller.control_period)