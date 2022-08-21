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
        self.wiring = {
            lambda: self._control.battery.value <= Config.LOW_VOLTAGE: self.low_voltage,
            lambda: self._control.ultrasonic.value <= 200: self.obstacle,  # mm
            # TODO: lift, docking
        }
        self.high_p_actions_kwargs = {'origin': self, 'priority': Priority.HIGH, 'same_actions_limit': 1, 'abort_previous': True}

    def low_voltage(self):
        self.logger.info(f'{self.__class__.__name__}->{self._control.battery.value}V > low power')
        # TODO: LOUD COMPLAIN, DOCKING

    def obstacle(self):
        self.perform(engine.TurnLeft(duration=2, justification=f'{self.__class__.__name__}->{self._control.ultrasonic.value}mm > Avoiding obstacle.', **self.high_p_actions_kwargs))
        # TODO: engine not running go backward?
