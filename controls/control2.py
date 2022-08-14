import time
import random
from enum import Enum

from lib.utils import who
from lib.threading2 import ComponentThread
from actuators import engine
from actuators.action import Priority, Result


class Mood(Enum):
    IDLE = 0,
    EXPLORE = 1,


class Control2(ComponentThread):
    """
        Neo Cortex.
        Periodically monitor sensors (via self.controls / ArchyCortex) and make LOW-PRIORITY decisions based on higher cognitive functions:
        * camera, speech, ...
        Remember traveled distance and try to perform reverse.
    """
    def __init__(self, period, control) -> None:
        super().__init__(period)
        self._current_action = None
        self._control = control
        self._mood = Mood.IDLE
        self.priority = Priority.LOW
        self.performing = ''

    def iterate(self) -> None:
        self.performing = ''
        self._mood = self.decide()
        self.logger.debug(f'{who(self)} decision: {self._mood}')
        self.perform()

        delay = self.period - (time.time() - self.last_iteration_time)
        self.logger.debug(f'{who(self)} finished, waiting {delay}s for new iteration.')
        time.sleep(delay)  # throttling

    def decide(self) -> Mood:
        match self._mood:
            case Mood.IDLE:
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[9, 1])[0]  # 10% chance to start explore
            case Mood.EXPLORE:
                if self._current_action.result == Result.ABORTED:
                    return Mood.IDLE                                                 # TODO: try reverse the failed action?
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[1, 9])[0]  # 10% chance to stop explore
            case _:
                assert False

    def perform(self) -> None:
        match self._mood:
            case Mood.IDLE:
                self.idle()
            case Mood.EXPLORE:
                self.explore()
            case _:
                assert False

    def idle(self):
        # TODO: self._control.engine.is_running > put stop?
        self._current_action = engine.Stop(self.priority, self.period)
        self.performing = f'Idling: stopping engine for {self.period}s.'
        self._control.perform(self._control.engine, self._current_action, self.performing)

    def explore(self):
        # TODO: change direction somehow smart
        self._current_action = engine.Start(self.priority, self.period)
        self.performing = f'Exploring: driving forward for {self.period}s.'
        self._control.perform(self._control.engine, self._current_action, self.performing)

    @property
    def state(self) -> str:
        return f'{super().state} {self._mood} {self.performing}'
