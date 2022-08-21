from sensors.sensor import Sensor
from lib.utils import who_long


class Battery(Sensor):
    def __init__(self, **kwargs):  # FIXME: needed?
        super().__init__(**kwargs)

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        value = 0  # FIX ME
        return value

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}V'
