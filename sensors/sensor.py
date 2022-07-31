import logging
import time
from enum import Enum
from threading import Thread, Condition, Event
from abc import ABC, abstractmethod

from control.control import Control


class Sensor(Thread, ABC):
    """
        Sensors job is to periodically:
         * read raw values from sensor
         ** process raw values = filter out deviations
         ** process data = create some (likely EMERGENCY priority) actions for actuators
         * on demand give the latest (processed) sensor value
    """

    def __init__(self, samples: int, period: float, control: Control) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.period = period
        self.control = control
        self.event_stop = Event()                   # to terminate the thread eventually
        self.raw_values = []  # FIXME: samples size of the window
        self.values = []  # FIXME: samples size of the window
        self.last_value_time: float = 0

    @property
    def value(self):
        return self.values[-1] if self.values else None

    def run(self):
        """ Sensor reading and data processing thread."""
        self.logger.info(f'{self.__class__.__name__} thread running.')

        while not self.event_stop.is_set():
            self.process_raw_value(self._read_raw_value())
            self.control.process_data(self)
            time.sleep(self.period)

        self.logger.info(f'{self.__class__.__name__} thread ended.')

    def stop(self):
        """ Make the "Sensor reading and data processing thread" to finish. """
        self.event_stop.set()                               # Stop getting actions from the queue.

    @abstractmethod
    def _read_raw_value(self):
        pass

    def process_raw_value(self, raw):
        # TODO: filter-out deviations
        pass
