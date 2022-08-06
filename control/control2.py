import time
from abc import ABC, abstractmethod

from lib.utils import who
from lib.threading import LoggingExceptionsThread
from actuators import engine, terminal, action


class Control2(LoggingExceptionsThread):
    """
        Paleo Cortex.
        Periodically monitor sensors (via self.control / ArchyCortex), make NON-EMERGENCY reactions.
        * evasive maneuvers
        * complains: low battery (docking later), ...?
    """
    def __init__(self, period, control) -> None:
        super().__init__()
        self.priority = action.Priority.HIGH
        self.period = period
        self._control = control

    def iterate(self):
        # self.logger.info(f'{who(self)} decision: None')
        # TODO: process sensor values from control
        # TODO: decide actions via control
        time.sleep(self.period)
