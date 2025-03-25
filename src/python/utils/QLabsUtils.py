import numpy
import time

from qvl.qlabs import QuanserInteractiveLabs
from devtoolkit.Log4P import Log4P

PI = numpy.pi
LOG_SOURCE = "QlabUtils"

class QLabsUtils:
    
    
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_qlab(address):
        logger = Log4P(enable_level = True,
                       enable_timestamp = True,
                       enable_source = True,
                       source = "QlabUtils")
        logger.info("Connecting to virtual environment...")
        quanser_interactive_labs = QuanserInteractiveLabs()
        quanser_interactive_labs.open(address)
        logger.info("Virtual environment connected.")
        logger.info("Formatting virtual environment...")
        quanser_interactive_labs.destroy_all_spawned_actors()
        logger.info("Virtual environment formatted.")
        return quanser_interactive_labs
    