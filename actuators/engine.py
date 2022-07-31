from actuators.action import Action
from actuators.actuator import Actuator


class Engine(Actuator):
    """
        * Performs drive / stop actions on the motors.
        * All motor actions are performed exclusively on the same thread to ensure serialisation / prioritisation.
    """
    def __init__(self) -> None:
        super().__init__()
        self.speed = 0  # TODO
        self.angle = 0  # TODO


class Start(Action):
    def execute(self):
        pass  # TODO: real engine start action


class Stop(Action):
    def execute(self):
        pass  # TODO: engine start action
