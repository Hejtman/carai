from actuators.engine import Engine


class CarAI:
    """
    Car HW = sensors + actuators

    Artificial Intelligence:
    * sensory read > making an decision for action > performing action

    Implemented as: Producer / Consumer design pattern:
    * Producer - produces actions based on sensory read (sensor + ai)
    * Consumer - performs actions from the priority queue (actuator)
    """

    def __init__(self):
        """ Each actuator has his own thread to ensure only one action per actuator at any time. """
        super().__init__()
        self.engine = Engine()

    def start(self) -> int:
        """ Start actuators threads. """
        self.engine.start()
        return 0
