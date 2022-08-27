# TODO: from statistic import mode
from sensors.sensor import Sensor
from lib.utils import who_long


try:
    from robot_hat import Ultrasonic as Ultrasonic_, Pin  # noqa
except ModuleNotFoundError:
    from fakes.ultrasonic import Ultrasonic as Ultrasonic_, Pin


class Ultrasonic(Sensor):
    MIN = 0.1
    MAX = 9999  # 100m

    def __init__(self, **kwargs):  # FIXME: needed?
        super().__init__(**kwargs)
        self._ultrasonic = Ultrasonic_(trig=Pin('D2'),
                                       echo=Pin('D3'))

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        return self._ultrasonic.read(times=1)

    def process_raw_value(self, raw) -> None:
        # FIXME: filter-out deviations
        if not self.values:
            self.values.append(raw)
            return

        if self.MIN <= raw <= self.MAX:
            self.values[0] = raw
        else:
            self.values[0] = self.MAX

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}mm'
