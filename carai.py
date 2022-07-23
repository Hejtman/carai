from hw import HW
from actuators.engine import EngineActionThread


class CarAI(HW):
    """
    Car instance:
    * HW: sensors + actuators
    * SW: read data > process > perform
    sensor 1 >read> decide action >write> actuator 1
    sensor 2 >read> decide action >write> actuator 1

    Implemented as Producer/Consumer design pattern.
    * Producer - produces actions based on sensory read
    * Consumer - performs actions from the queue
    """

    """ Puts all the HW and AI into one entity. """
    def __init__(self):
        """ Each actuator has his own thread to ensure only one action per actuator is performed at any time. """
        super().__init__()
        self.engine = EngineActionThread()

    def start(self) -> int:
        """ Start actuators threads. """
        self.engine.start()
        return 0
