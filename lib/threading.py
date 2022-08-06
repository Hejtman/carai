import logging
from threading import Thread, Event
from abc import ABC, abstractmethod

from lib.utils import who


class LoggingThread(ABC, Thread):
    """
        Extends standard Thread for logging thread's: start, stop and dying by exception.
        Adds graceful way to stop the thread (via calling stop() method as the Thread start() counterpart).
    """
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.event_stop = Event()

    def run(self):
        """ Thread's main loop. """
        self.logger.info(f'{who(self)} thread running.')

        while not self.event_stop.is_set():
            self._iterate()

        self.logger.info(f'{who(self)} thread ended.')

    def _iterate(self):
        try:
            self.iterate()
        except:
            self.logger.exception(f'{who(self)} thread died by exception:')
            raise

    @abstractmethod
    def iterate(self):
        """ Repeatedly called within the thread's main loop. """
        pass

    def stop(self):
        """ Allow the thread to gracefully finish by stopping calling iterate(). """
        self.event_stop.set()


class LoggingExceptionsThread(LoggingThread, ABC):
    """ LoggingThread logging + ignoring exceptions. """
    def _iterate(self):
        try:
            self.iterate()
        except:  # log and ignore
            self.logger.exception(f'{who(self)} thread died by exception:')
