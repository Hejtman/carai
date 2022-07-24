from abc import ABC, abstractmethod
from enum import Enum
from time import time


class Actuator:  # Just stored (as pointer) here, used / implemented elsewhere
    pass


class Result(Enum):
    FINISHED = 0
    ABORTED = 1


class Action(ABC):
    def __init__(self, actuator: Actuator, priority: int, duration: float):
        self.actuator: Actuator = actuator
        self.priority: int = priority
        self.duration: float = duration
        self.start_time: float = 0
        self.end_time: float = 0
        self.result = None

    def execute_wrapper(self) -> None:
        self.logger.debug(f'{self.actuator.__class__.__name__} executing {self}')
        self.start_time = time()
        self.execute()
        self.end_time = time()

        if end_time - start_time < self.duration:
            self.logger.info(f'{self.actuator.__class__.__name__} execution {self} aborted after {duration}s')
            self.result = ABORTED
        else:
            self.logger.debug(f'{self.actuator.__class__.__name__} execution {self} finished after {duration}s')
            self.result = FINISHED

    @abstractmethod
    def execute(self) -> None:
        pass
