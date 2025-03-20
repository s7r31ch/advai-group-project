import time
import numpy

from qvl.walls import QLabsWalls
from qvl.qbot_platform_flooring import QLabsQBotPlatformFlooring
from utils.LogUtils import LogUtils

PI=numpy.pi
LOG_SOURCE = "EnvironmentUtils"

class EnvironmentUtils:
    
    def __init__(self):
        pass
    
    @staticmethod
    def set_floor(qlab):
        LogUtils.log(LOG_SOURCE, "正在生成地板...")
        qlabs_qbot_platform_flooring = QLabsQBotPlatformFlooring(qlab)
        qlabs_qbot_platform_flooring.spawn(location = [-0.6,-0.6,0], rotation = [0,0,0], scale = [1,1,1], configuration = 5, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [0.6,1.8,0], rotation = [0,0,-PI/2], scale = [1,1,1], configuration = 0, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [1.8,-0.6,0], rotation = [0,0,PI], scale = [1,1,1], configuration = 0, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [-0.6,-1.8,0], rotation = [0,0,PI/2], scale = [1,1,1], configuration = 0, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [-1.8,0.6,0], rotation = [0,0,0], scale = [1,1,1], configuration = 0, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [-0.6,0.6,0], rotation = [0,0,0], scale = [1,1,1], configuration = 1, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [0.6, 0.6,0], rotation = [0,0,-PI/2], scale = [1,1,1], configuration = 1, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [0.6,-0.6,0], rotation = [0,0,PI], scale = [1,1,1], configuration = 1, waitForConfirmation= False)
        qlabs_qbot_platform_flooring.spawn(location = [-0.6,-0.6,0], rotation = [0,0,PI/2], scale = [1,1,1], configuration = 1, waitForConfirmation= False)
        LogUtils.log(LOG_SOURCE, "地板生成完毕...")

    @staticmethod
    def set_wall(qlab):
        LogUtils.log(LOG_SOURCE, "正在生成墙体...")
        qlabs_walls = QLabsWalls(qlab)
        qlabs_walls.spawn(location=[2, 1.2, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[2, 0, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[2, -1.2, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[-2, 1.2, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[-2, 0, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[-2, -1.2, 0.1], rotation=[0, 0, 0])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[1.2, 2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[0, 2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[-1.2, 2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[1.2, -2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[0, -2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        qlabs_walls.spawn(location=[-1.2, -2, 0.1], rotation=[0, 0, PI/2])
        qlabs_walls.set_enable_dynamics(True)
        LogUtils.log(LOG_SOURCE, "墙体生成完毕...")
