import time
from abc import ABC, abstractmethod

from lib.threading2 import LoggingExceptionsThread


class Sensor(LoggingExceptionsThread, ABC):
    """
        Sensors job is to periodically:
         * read raw values from sensor
         ** process raw values = filter out deviations
         ** process data = create some (likely EMERGENCY priority) actions for actuators
         * on demand give the latest (processed) sensor value
    """
    def __init__(self, samples: int, period: float, control) -> None:
        super().__init__()
        self.period = period
        self._control = control
        self.raw_values = []  # FIXME: samples size of the window
        self.values = []  # FIXME: samples size of the window
        self.last_value_time: float = 0

    @property
    def value(self):
        return self.values[-1] if self.values else None

    def iterate(self):
        """ Sensor reading and data processing iteration (which gets repeatedly called while this thread lives). """
        self.process_raw_value(self._read_raw_value())
        self._control.process_data(self)
        time.sleep(self.period)

    @abstractmethod
    def _read_raw_value(self):
        pass

    def process_raw_value(self, raw):
        # FIXME: filter-out deviations
        if not self.values:
            self.values.append(raw)
        else:
            self.values[0] = raw
