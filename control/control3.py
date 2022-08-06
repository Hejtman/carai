import time
import random
from enum import Enum

from lib.utils import who
from lib.threading import LoggingExceptionsThread
from actuators import engine, action


class Mood(Enum):
    IDLE = 0,
    EXPLORE = 1,


class Control3(LoggingExceptionsThread):
    """
        Neo Cortex.
        Periodically monitor sensors (via self.control / ArchyCortex) and make LOW-PRIORITY decisions based on higher cognitive functions:
        * camera, speech, ...
    """
    def __init__(self, period, control) -> None:
        super().__init__()
        self.period = period
        self._current_action = None
        self._control = control
        self._mood = Mood.IDLE
        self.priority = action.Priority.LOW

    def iterate(self):
        start_time = time.time()

        self._mood = self.decide()
        self.logger.debug(f'{who(self)} decision: {self._mood}')
        self.perform()

        delay = self.period - (time.time() - start_time)
        self.logger.debug(f'{who(self)} finished, waiting {delay}s for new iteration.')
        time.sleep(delay)  # throttling

    def decide(self) -> Mood:
        match self._mood:
            case Mood.IDLE:
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[9, 1])[0]  # 10% chance to start explore
            case Mood.EXPLORE:
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[1, 9])[0]  # 10% chance to stop explore
            case _:
                print(self._mood)
                assert False

    def perform(self) -> None:
        match self._mood:
            case Mood.IDLE:
                pass
            case Mood.EXPLORE:
                self.explore()
            case _:
                assert False

    def explore(self):
        # TODO: random? direction
        if not self._current_action or self._current_action.result == action.Result.FINISHED:
            self._current_action = engine.Start(self.priority, self.period)
            self._control.perform(self._control.engine, self._current_action, f'Exploring: driving forward for {self.period}s.')
        else:
            print(f'xxxxxxxxxxxx{self._current_action.result}')
