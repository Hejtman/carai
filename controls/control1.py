import time

from lib.threading2 import ComponentThread
from actuators import action


class Control1(ComponentThread):
    """
        Paleo Cortex.
        Periodically monitor sensors (via self.controls / ArchyCortex), make NON-EMERGENCY reactions.
        * detect: lift?
        * evasive maneuvers
        * complains: low battery (docking later), ...?
    """
    def __init__(self, period, control) -> None:
        super().__init__(period)
        self.priority = action.Priority.HIGH
        self._control = control

    def iterate(self):
        # self.logger.info(f'{who(self)} decision: None')
        # TODO: process sensor values from controls
        # TODO: decide actions via controls
        time.sleep(self.period)
