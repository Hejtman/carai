from actuators.action import Action
from actuators.actuator import Actuator


class Terminal(Actuator):
    def __init__(self) -> None:
        super().__init__()


class ShutDown(Action):
    def execute(self) -> None:
        print('SYSTEM SHUTTING DOWN!!!')  # TODO: real engine start action
