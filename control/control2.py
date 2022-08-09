import time

from lib.threading2 import LoggingExceptionsThread
from actuators import action


class Control2(LoggingExceptionsThread):
    """
        Paleo Cortex.
        Periodically monitor sensors (via self.control / ArchyCortex), make NON-EMERGENCY reactions.
        * detect: lift?
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
