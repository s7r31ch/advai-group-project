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
        LogUtils.log(LOG_SOURCE, "Connecting to virtual environment...")
        quanser_interactive_labs = QuanserInteractiveLabs()
        quanser_interactive_labs.open(address)
        LogUtils.log(LOG_SOURCE, "Virtual environment connected.")
        LogUtils.log(LOG_SOURCE, "Formatting virtual environment...")
        quanser_interactive_labs.destroy_all_spawned_actors()
        LogUtils.log(LOG_SOURCE, "Virtual environment formatted.")
        return quanser_interactive_labs
    