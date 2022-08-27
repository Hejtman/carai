from sensors.sensor import Sensor
from lib.utils import who_long

try:
    from robot_hat import ADC  # noqa
except ModuleNotFoundError:
    from fakes.adc import ADC


class Battery(Sensor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        return round(ADC('A4').read() / 4096.0 * 3.3 * 3, 2)

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}V'
