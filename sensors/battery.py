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

    def process_raw_value(self, raw) -> None:
        if raw <= 0:
            raw = 9999

        # FIXME: filter-out deviations
        if not self.values:
            self.values.append(raw)
        else:
            self.values[0] = raw


    @property
    def state(self) -> str:
        return f'{super().state} {self.value}V'
