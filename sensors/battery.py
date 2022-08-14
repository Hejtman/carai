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


BATTERIES = 3                        # using 3 LIFEPO4 batteries
NORMAL_VOLTAGE = 3.2 * BATTERIES     # https://batteryfinds.com/whats-lifepo4-over-discharge-lifepo4-overcharge/
LOW_VOLTAGE = 3 * BATTERIES
VERY_LOW_VOLTAGE = 2.7 * BATTERIES
