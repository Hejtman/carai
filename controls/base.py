import logging
import time
from abc import ABC, abstractmethod

from lib.utils import who_long, time2next


class Component(ABC):
    """ Logs + state exceptions, but without implementing threading loop periodically calling _iterate(). """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.last_exception = None

    def _iterate(self):
        try:
            self.iterate()
        except Exception as ex:  # log and remember
            self.last_exception = ex
            self.logger.exception(f'{who_long(self)} thread got an unhandled exception:')

    @property
    def state(self) -> str:
        return f'💥{self.last_exception}' if self.last_exception else '✅'

    @abstractmethod
    def iterate(self):
        pass


class ComponentPeriod(Component, ABC):
    """ Component + period reflected in state + sleep to finish a period. """
    def __init__(self, period):
        super().__init__()
        self.period = period
        self.iteration_time: float = 0

    def _iterate(self):
        self.iteration_time = time.time()
        super()._iterate()
        time.sleep(time2next(self.period, self.iteration_time))

    @property
    def state(self) -> str:
        hour = 3600  # FIXME: time interval hour
        return f'{super().state}' if time2next(self.period, self.iteration_time) \
            else f'⌛ {time.time()-self.iteration_time}' if time.time()-self.iteration_time < hour \
            else '❌'


class ControlBase(ComponentPeriod, ABC):
    """ ComponentPeriod + last_action.justification in state (cleared when last_action finished). """
    def __init__(self, period, control) -> None:
        super().__init__(period)
        self._control = control
        self.last_action = None
        self.wiring = {}

    def _iterate(self):
        super()._iterate()
        if self.last_action and self.last_action.is_finished:
            self.last_action = None

    def iterate(self):
        [handler() for condition, handler in self.wiring.items() if condition()]

    def perform(self, action) -> None:
        next(actuator for actuator in self._control.actuators if actuator.put(action))
        self.last_action = action

    @property
    def state(self) -> str:
        return f'{super().state} {self.last_action.justification if self.last_action else ""}'
