# TODO: from statistic import mode
import random
from sensors.sensor import Sensor
from lib.utils import who_long


class Ultrasonic(Sensor):
    def __init__(self, **kwargs):  # FIXME: needed?
        super().__init__(**kwargs)

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        value = random.randint(0, 1000)  # FIX ME
        return value

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}mm'
