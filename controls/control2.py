import random
from enum import Enum

from controls.base import ControlBase
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who_long
from actuators import engine
from actuators.action import Priority, Result


class Mood(Enum):
    IDLE = 0,
    EXPLORE = 1,


class Control2(ControlBase, LoggingExceptionsThread):
    """
        Neo Cortex.
        Periodically monitor sensors (via self.controls / ArchyCortex) and make LOW-PRIORITY decisions based on higher cognitive functions:
        * camera, speech, ...
        Remember traveled distance and try to perform reverse.
    """
    def __init__(self, period, control) -> None:
        super().__init__(period, control)
        LoggingExceptionsThread.__init__(self)
        self._mood = Mood.IDLE
        self.low_p_actions_kwargs = {'origin': self, 'priority': Priority.LOW, 'same_actions_limit': 2, 'abort_previous': False}

    def decide(self) -> Mood:
        match self._mood:
            case Mood.IDLE:
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[9, 1])[0]  # 10% chance to start explore
            case Mood.EXPLORE:
                if self.last_action and self.last_action.result == Result.ABORTED:
                    return Mood.IDLE                                                 # TODO: try reverse the failed action?
                return random.choices([Mood.IDLE, Mood.EXPLORE], weights=[1, 9])[0]  # 10% chance to stop explore
            case _:
                assert False

    def iterate(self) -> None:
        self._mood = self.decide()
        self.logger.debug(f'{who_long(self)} decision: {self._mood}')
        match self._mood:
            case Mood.IDLE:
                self.idle()
            case Mood.EXPLORE:
                self.explore()
            case _:
                assert False

    def idle(self):
        # TODO: self._control.engine.is_running > put stop?
        self.perform(engine.Stop(duration=self.period, justification=f'Idling: stopping engine for {self.period}s.', **self.low_p_actions_kwargs))

    def explore(self):
        # TODO: change direction somehow smart
        self.perform(engine.MoveStraight(duration=self.period, justification=f'Exploring: driving forward for {self.period}s.', **self.low_p_actions_kwargs))

    @property
    def state(self) -> str:  # FIXME: needed?
        return f'{super().state} {self._mood}'
