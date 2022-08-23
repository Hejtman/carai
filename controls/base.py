import logging
import time
from datetime import timedelta
from abc import ABC, abstractmethod

from lib.utils import who_long, time2next


class Component(ABC):
    """ Logs + state exceptions, but without implementing periodic loop over iterate_wrapper(). """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.last_exception = None

    def iterate_wrapper(self):
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
    """ Component + sleep until next iteration/period + state reflects if iterate_wrapper was called within the given period. """
    def __init__(self, period):
        super().__init__()
        self.period = period
        self.iteration_time: float = 0

    def iterate_wrapper(self):
        self.iteration_time = time.time()
        super().iterate_wrapper()
        time.sleep(time2next(self.period, self.iteration_time))

    @property
    def state(self) -> str:
        return f'{super().state}' if time2next(self.period, self.iteration_time) \
            else f'⌛ {time.time()-self.iteration_time}' if time.time()-self.iteration_time < timedelta(hours=1).total_seconds() \
            else '💀'


class ControlBase(ComponentPeriod):
    """ ComponentPeriod performing conditioned actions in each iteration + reflecting these in state """
    def __init__(self, period, control) -> None:
        super().__init__(period)
        self._control = control
        self.performing_actions = []
        self.conditional_actions: tuple[callable, callable] = tuple()

    def iterate_wrapper(self):
        self.performing_actions = [action for action in self.performing_actions if not action.is_processed]
        super().iterate_wrapper()

    def iterate(self):
        [self.perform(action) for condition, action in self.conditional_actions if condition()]

    def perform(self, action) -> None:
        self.performing_actions.append(action)
        any(actuator.put(action) for actuator in self._control.actuators)

    @property
    def state(self) -> str:
        return f'{super().state} {", ".join(a.justification for a in self.performing_actions)}'
