import logging
from time import time
from abc import ABC, abstractmethod
from enum import IntEnum

from lib.utils import who_long


class Priority(IntEnum):
    LOW = 1000      # Neo   cortex - menu, games, interactions
    HIGH = 100      # Paleo cortex - sensory/camera processing, location/map creation, RC
    EMERGENCY = 10  # Archy cortex - sensory readings > emergency levels


class Result(IntEnum):
    NOT_SET = -1
    FINISHED = 0
    ABORTED = 1
    FAILED = 2


class Action(ABC):
    class Event:
        """ Timestamps container. Set by Actuator while processing the action. """
        def __init__(self) -> None:
            self.queued: float = 0          # put into actuators action queue
            self.start: float = 0           # execution started
            self.execution: float = 0       # execution finished
            self.end: float = 0             # aborted or action duration time reached > task result set  > actuator freed to start execution of another action (from action priority queue)

    def __init__(self, origin: any, priority: int, duration: float, justification: str = '', same_actions_limit: int = 0, abort_previous: bool = False) -> None:
        self.origin: any = origin           # which Control made the decision
        self.priority: int = priority       # for sorting on actuators action_priority_queue
        self.duration: float = duration     # minimal time before another action execution allowed = execution + wait(delay) [if action execution aborted, delay is interrupted]
        self.justification: str = justification
        self.same_actions_limit: int = same_actions_limit   # over reacting prevention > actuator will refuse to put this task into queue if already processing this limit of the same tasks
        self.abort_previous: bool = abort_previous
        self.event: Action.Event = Action.Event()
        self.result: Result = Result.NOT_SET
        self.logger = logging.getLogger(__name__)

    @property
    def time_spent(self) -> float:
        assert self.event.end
        return self.event.end - self.event.start

    @property
    def is_finished(self) -> bool:
        return self.result == Result.FINISHED

    def __gt__(self, other) -> bool:  # priority comparison used when action put into priority queue for execution
        return self.priority > other.priority

    def __ge__(self, other) -> bool:  # FIXME: needed?
        return self.priority >= other.priority

    def __eq__(self, other) -> bool:  # is it the same action? (implementation + duration)
        return other and (self.__class__, self.duration) == (other.__class__, other.duration)

    def execute_wrapper(self, actuator) -> None:
        self.logger.debug(f'{who_long(self)} is being executed.')
        self.event.start = time()

        # noinspection PyBroadException
        try:
            self.execute(actuator)
        except:                             # LOG & FORGET: A single Action execution shall not bring down an entire Actuator
            self.logger.exception(f'{who_long(self)} execution died by exception:')
            self.result = Result.FAILED
        else:
            self.event.execution = time()
            execution_duration = self.event.execution - self.event.start
            timeout = self.duration - execution_duration
            self.logger.debug(f'{who_long(self)} execution took {execution_duration}, now waiting {timeout}s to finish it.')

            aborted = actuator.lock.wait(timeout)    # wait until action duration reached (or action aborted prematurely from outer thread)

            self.result = Result.ABORTED if aborted else Result.FINISHED
            self.event.end = time()
            level = logging.DEBUG if self.result == Result.FINISHED else logging.INFO if self.result == Result.ABORTED else logging.ERROR
            self.logger.log(level, f'{who_long(self)} execution of {self.__dict__} result={self.result} after {self.time_spent}s')

    @abstractmethod
    def execute(self, actuator) -> None:
        pass


class NoneAction(Action):
    """ No Operation Action. Useful to unblock thread waiting for an Action to be put into empty execution queue."""
    def __init__(self) -> None:
        super().__init__(origin=None, priority=0, duration=0)

    def execute(self, actuator) -> None:
        pass
