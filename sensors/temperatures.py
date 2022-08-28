from sensors.sensor import Sensor
from lib.utils import who_long

try:
    from gpiozero import CPUTemperature  # noqa
except ModuleNotFoundError:
    from fakes.cputemperature import CPUTemperature


class CPU(Sensor):
    def __init__(self, **kwargs):
        super().__init__(minimum=0.0, maximum=1000, invalid=1000, **kwargs)
        self.cpu = CPUTemperature()

    def _read_raw_value(self) -> float:
        self.logger.debug(f'Reading {who_long(self)}')
        return self.cpu.temperature

    @property
    def state(self) -> str:
        return f'{super().state} {self.value}℃'

    """
    class Temperatures:
        def __init__(self, period):
            super().__init__(period)
            self.components = []
    
        def start(self):
            pass
        
        def stop(self):
            pass
    
        @property
        def state(self):
            pass        
    """
