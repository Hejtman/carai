# TODO: from statistic import mode
import random
from sensors.sensor import Sensor
from lib.utils import who


class Ultrasonic(Sensor):
    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who(self)}')
        value = random.randint(0, 1000)  # FIX ME
        return value

    @property
    def state(self) -> str:
        return f'{super(Sensor, self).state} {self.value}mm'
