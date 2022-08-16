from sensors.sensor import Sensor
from lib.utils import who


class Battery(Sensor):
    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who(self)}')
        value = 0  # FIX ME
        return value

    @property
    def state(self) -> str:
        return f'{super(Sensor, self).state} {self.value}V'

