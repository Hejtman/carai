#from statistic import mode
from sensors.sensor import Sensor
from lib.utils import who


class Ultrasonic(Sensor):
    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who(self)}')
        value = 0  # FIX ME
        return value
