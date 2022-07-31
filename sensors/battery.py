from sensors.sensor import Sensor


class Battery(Sensor):
    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {self.__class__.__name__}')
        value = 0  # FIX ME
        return value
