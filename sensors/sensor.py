from abc import ABC, abstractmethod

from collections import deque
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who
from controls.base import ComponentPeriod


class Sensor(ComponentPeriod, LoggingExceptionsThread, ABC):
    """
        Sensors job is to periodically:
         * read raw values from sensor
         * process raw values = filter out deviations
         * on demand give the latest (processed) sensor value and store given amount (store_last_values) of raw and processed last values
    """
    def __init__(self, period: float, store_last_values: int = 100) -> None:
        ComponentPeriod.__init__(self, period)
        LoggingExceptionsThread.__init__(self)
        self.raw_values = deque(maxlen=store_last_values)
        self.values = deque(maxlen=store_last_values)

    @property
    def value(self) -> [any, None]:
        return self.values[-1] if self.values else None

    def iterate(self) -> None:
        """ Sensor reading and data processing iteration (which gets periodically called while this thread lives). """
        raw_value = self.read_raw_value()
        self.raw_values.append(raw_value)
        self.process_raw_value(raw_value)

    @abstractmethod
    def read_raw_value(self) -> any:
        pass

    def process_raw_value(self, raw) -> None:
        # FIXME: filter-out deviations
        self.values.append(raw)

    def stop(self):
        super().stop()
        self.logger.debug(f'{who(self)}\nraw_values={self.raw_values}\nvalues={self.values}')

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}'


class SensorControl(Sensor, ABC):
    """ Sensor + ask control to process obtained value immediately when obtained to create/perform some (likely EMERGENCY priority) actions for actuators. """
    def __init__(self, period: float, control, store_last_values: int = 100) -> None:
        super().__init__(period, store_last_values)
        self._control = control

    def process_raw_value(self, raw) -> None:
        super().process_raw_value(raw)
        self._control.process_data(self)


class SensorControlRange(SensorControl, ABC):
    """ SensorControl + ask control to process obtained values only when within given range. """
    def __init__(self, period: float, control, minimum, maximum, store_last_values: int = 100) -> None:
        super().__init__(period, control, store_last_values)
        self.maximum = maximum
        self.minimum = minimum

    def process_raw_value(self, raw) -> None:
        if self.minimum <= raw <= self.maximum:
            super().process_raw_value(raw)
