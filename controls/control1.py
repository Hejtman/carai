from actuators.action import Priority
from controls.base import ControlBase
from lib.threading2 import LoggingExceptionsThread
from config import Config
from actuators import engine


class Control1(ControlBase, LoggingExceptionsThread):
    """ Paleo Cortex role: Periodically monitor sensors to make NON-EMERGENCY reactions. """
    def __init__(self, period, control) -> None:
        super().__init__(period, control)
        LoggingExceptionsThread.__init__(self)
        self.actions_kwargs = {'origin': self, 'priority': Priority.HIGH, 'same_actions_limit': 1, 'abort_previous': True}

        self.conditional_actions = (
            # (lambda: self._control.battery.value <= Config.LOW_VOLTAGE, self.low_voltage),  # FIXME
            # (lambda: self._control.ultrasonic.value <= 200, engine.TurnLeft(duration=2, justification=f'{self._control.ultrasonic.value=}mm > Avoiding obstacle.', **self.actions_kwargs)),
            # TODO: lift, docking
        )
