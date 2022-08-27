from abc import ABC, abstractmethod

from lib.threading2 import LoggingExceptionsThread
from lib.utils import who
from controls.base import ComponentPeriod


class Sensor(ComponentPeriod, LoggingExceptionsThread, ABC):
    """
        Sensors job is to periodically:
         * read raw values from sensor
         ** process raw values = filter out deviations
         ** process data = create some (likely EMERGENCY priority) actions for actuators
         * on demand give the latest (processed) sensor value
    """
    def __init__(self, samples: int, period: float, control) -> None:
        ComponentPeriod.__init__(self, period)
        LoggingExceptionsThread.__init__(self)
        self._control = control
        self.raw_values = []  # FIXME: samples size of the window
        self.values = []  # FIXME: samples size of the window

    @property
    def value(self) -> [float]:
        return self.values[-1] if self.values else -1

    def iterate(self) -> None:
        """ Sensor reading and data processing iteration (which gets repeatedly called while this thread lives). """
        raw_value = self._read_raw_value()
        self.raw_values.append(raw_value)
        self.process_raw_value(raw_value)
        self._control.process_data(self)  # FIXME: only if value is valid?

    @abstractmethod
    def _read_raw_value(self) -> None:
        pass

    def process_raw_value(self, raw) -> None:
        # FIXME: filter-out deviations
        if not self.values:
            self.values.append(raw)
        else:
            self.values[0] = raw

    def stop(self):
        super().stop()
        self.logger.debug(f'{who(self)}\nraw_values={self.raw_values}\nvalues={self.values}')
