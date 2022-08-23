import logging
from threading import Thread, Event
from abc import ABC, abstractmethod

from lib.utils import who_long


class LoggingExceptionsThread(Thread, ABC):
    """
        Extends standard Thread for start, stop, logging exceptions and giving state string.
        Adds graceful way to stop the thread (via calling stop() method as the Thread start() counterpart).
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.last_exception = None
        self.event_stop = Event()

    def run(self):
        """ Thread's main loop. """
        self.logger.info(f'{who_long(self)} thread running.')

        while not self.event_stop.is_set():
            self.iterate_wrapper()

        self.logger.info(f'{who_long(self)} thread ended.')

    def iterate_wrapper(self):
        try:
            self.iterate()
        except Exception as ex:  # log and remember
            self.last_exception = ex
            self.logger.exception(f'{who_long(self)} thread got unhandled exception.')

    @abstractmethod
    def iterate(self):
        """ Repeatedly called within the thread's main loop. """
        pass

    def stop(self):
        """ Allow the thread to gracefully finish by stopping calling iterate(). """
        self.event_stop.set()

    @property
    def state(self) -> str:
        """ This method is called from outer thread. Variables might change asynchronously. """
        return f'💥{self.last_exception}' if self.last_exception else '❌' if self.event_stop.is_set() else '✅'
