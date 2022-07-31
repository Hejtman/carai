from control.control import Control
from sensors.battery import Battery
from sensors.ultrasonic import Ultrasonic
from actuators.engine import Engine
from actuators.terminal import Terminal


class CarAI:
    """
        HW = sensors + actuators
        SW = sensor >DATA> control >ACTION> actuator

        Implemented as: Producer / Consumer design pattern:
        * Producer - produces actions based on sensory read (sensor + decision making)
        * Consumer - performs actions from the priority queue (actuator)
    """
    def __init__(self):
        super().__init__()
        self.control = Control()
        self.control.sensors = [Battery(samples=10, period=10, control=self.control),
                                Ultrasonic(samples=10, period=0.1, control=self.control)]
        self.control.actuators = [Terminal(), Engine()]

    def start(self) -> None:
        self.control.start()


if __name__ == '__main__':
    c = CarAI()
    c.start()
