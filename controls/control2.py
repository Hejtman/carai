import time
import random
from enum import Enum

from controls.base import ControlBase
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who_long
from actuators import repro, voice
from actuators.action import Priority, Result


class Mood(Enum):
    IDLE = 0,
    EXPLORE = 1,
    INIT = 2


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
        self._mood = Mood.INIT
        self.actions_kwargs = {'origin': self, 'priority': Priority.LOW, 'same_actions_limit': 1, 'abort_previous': False}
        self.conditional_actions = (
            #(lambda: self._mood == Mood.INIT, repro.PlayX(duration=10, justification='Just play some testing sound.', **self.actions_kwargs)),
            #(lambda: self._mood == Mood.INIT, voice.SayHellow(duration=10, justification='Just play some testing sound.', **self.actions_kwargs)),
        )
        # [self.perform(action) for condition, action in self.conditional_actions if condition()]
        # engine.Stop(duration=self.period, justification=f'Idling: stopping engine for {self.period}s.', **self.actions_kwargs)
        # self.perform(engine.MoveStraight(duration=self.period, justification=f'Exploring: driving forward for {self.period}s.', **self.actions_kwargs))

    def iterate(self):
        super().iterate()
        if self._mood == Mood.INIT:
            time.sleep(10)
            self.perform(voice.SayHellow(duration=10, justification='Just to test voice.', **self.actions_kwargs))
            time.sleep(10)
            self.perform(repro.PlayX(duration=10, justification='Just to test playing some sound.', **self.actions_kwargs))
            time.sleep(10)
            self._mood = Mood.IDLE

    @property
    def state(self) -> str:
        return f'{super().state} {self._mood}'

"""
    def decide(self) -> Mood:
        match self._mood:
            case Mood.IDLE:  # FIXME: dict
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
"""
