import numpy
import time

from qvl.qlabs import QuanserInteractiveLabs
from utils.LogUtils import LogUtils

PI = numpy.pi
LOG_SOURCE = "QlabUtils"

class QLabsUtils:
    
    
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_qlab(address):
        LogUtils.log(LOG_SOURCE, "正在建立与实验环境的连接...")
        quanser_interactive_labs = QuanserInteractiveLabs()
        quanser_interactive_labs.open(address)
        LogUtils.log(LOG_SOURCE, "实验环境已连接")
        LogUtils.log(LOG_SOURCE, "正在清理实验环境...")
        quanser_interactive_labs.destroy_all_spawned_actors()
        LogUtils.log(LOG_SOURCE, "实验环境已清理完成")
        return quanser_interactive_labs
    