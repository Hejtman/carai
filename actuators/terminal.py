from abc import ABC
from actuators.action import Action
from actuators.actuator import Actuator


class TerminalAction(Action, ABC):
    pass


class Terminal(Actuator):
    def __init__(self) -> None:
        super().__init__(accepts=TerminalAction)


class ShutDown(TerminalAction):
    def execute(self, actuator: Terminal) -> None:
        print('SYSTEM SHUTTING DOWN!!!')  # TODO: real engine start action
