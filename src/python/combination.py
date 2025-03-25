import threading
from PIL import Image
import matplotlib.pyplot as plt

from utils.QLabsUtils import QLabsUtils
from utils.EnvironmentUtils import EnvironmentUtils
from utils.QBotUtils import QBotUtils
from devtoolkit.Log4P import Log4P
from devtoolkit.KeyboardMonitor import KeyboardMonitor
from controller.KeyboardController import KeyboardController
from controller.PIDController import PIDController
from nn.network.MyCNN import MyCNN
from nn.api.Classifier import Classifier

if __name__ == "__main__":
    
    MANUAL_CONTROL_PERIOD = 0.1
    PID_CONTROL_PERIOD = 0.05
    
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
    
    # Controller initialing
    keyboard_controller = KeyboardController(qbot = qbot,
                                             control_period = MANUAL_CONTROL_PERIOD)
    pid_controller = PIDController(qbot = qbot,
                                   control_period = PID_CONTROL_PERIOD)
    
    # CNN model loading
    myCNN = MyCNN(6)
    classifier = Classifier("src/resources/model_2025-03-22-184045.pth", myCNN)
    logger.info("CNN model loaded.")
    
    # 也就是说，前方有对控制方式的选择
    control_type = input("Select a control method: (m/a/p)\n")
    match control_type:
        case "m":
            controller = keyboard_controller
            logger.info("Manual control selected.")
        case "a":
            controller = pid_controller
            logger.info("Auto control selected.")
        case "p":
            controller = pid_controller
            logger.info("Programmed control selected.")
    
    # 主控制循环万岁
    while True:
        match control_type:
            # 前有手动控制
            case "m":
                key = keyboard_monitor.listen()
                if key is not None: controller.send(key)