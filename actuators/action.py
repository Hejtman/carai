from abc import ABC, abstractmethod
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1000      # Neo   cortex - menu, games, interactions
    HIGH = 100      # Paleo cortex - sensory/camera processing, location/map creation, RC
    EMERGENCY = 10  # Archy cortex - sensory readings > emergency levels


class Result(IntEnum):
    NOT_SET = -1
    FINISHED = 0
    ABORTED = 1


class Action(ABC):
    class Event:
        """ Timestamps container. Set by Actuator while processing the action. """
        def __init__(self):
            self.queued: float = 0          # put into actuators action queue
            self.start: float = 0           # execution started
            self.execution: float = 0       # execution finished
            self.end: float = 0             # aborted or action duration time reached > task result set  > actuator freed to start execution of another action (from action priority queue)

    def __init__(self, priority: int, duration: float):
        self.priority: int = priority       # for sorting on actuators action_priority_queue
        self.duration: float = duration     # minimal time before another action execution allowed = execution + wait(delay) [if action execution aborted, delay is interrupted]
        self.event: Action.Event = Action.Event()
        self.result: Result = Result.NOT_SET

    @property
    def time_spent(self) -> float:
        assert self.event.end
        return self.event.end - self.event.start

    # priority comparison happens when action put into priority queue for execution
    def __gt__(self, other):  # FIXME: +": Action" typehint when python allows (later 3.10 or 3.11)
        return self.priority > other.priority

    def __eq__(self, other):  # FIXME: +": Action" typehint when python allows (later 3.10 or 3.11)
        return self.priority == other.priority

    def __ge__(self, other):  # FIXME: +": Action" typehint when python allows (later 3.10 or 3.11)
        return self.priority >= other.priority

    @abstractmethod
    def execute(self) -> None:
        pass


class NoneAction(Action):
    """ No Operation Action. Useful to unblock thread waiting for an Action to be put into empty execution queue."""
    def __init__(self):
        super().__init__(priority=0, duration=0)

    def execute(self):
        pass
