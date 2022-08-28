# TODO: from statistic import mode
from sensors.sensor import Sensor
from lib.utils import who_long


try:
    from robot_hat import Ultrasonic as Ultrasonic_, Pin  # noqa
except ModuleNotFoundError:
    from fakes.ultrasonic import Ultrasonic as Ultrasonic_, Pin


class Ultrasonic(Sensor):
    def __init__(self, **kwargs):  # FIXME: needed?
        super().__init__(minimum=0.1, maximum=9999, invalid=9999, **kwargs)
        self._ultrasonic = Ultrasonic_(trig=Pin('D2'),
                                       echo=Pin('D3'))

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        return self._ultrasonic.read(times=1)

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}cm'
