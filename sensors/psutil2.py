import datetime
import psutil

from sensors.sensor import Sensor
from lib.utils import who_long


class PsUtil(Sensor):
    def __init__(self, period: float):
        super().__init__(period, store_last_values=1)
        self.psutil_process = psutil.Process()

    def read_raw_value(self) -> str:
        self.logger.debug(f'Reading {who_long(self)}')

        start = datetime.datetime.now()
#        with self.psutil_process.oneshot():  # FIXME: expensive diagnostic
#            proces = f'{self.psutil_process.cpu_percent()}% {1+len(self.psutil_process.children())}p{self.psutil_process.num_threads()}t {round(self.psutil_process.memory_percent(), 1)}%'
#            proces_extra = f'{self.psutil_process.pid}: {self.psutil_process.children()}'
        cpu = f'{psutil.cpu_percent(interval=None)}% {psutil.cpu_freq(percpu=False).current} {psutil.sensors_temperatures().get("cpu_thermal")[0].current}℃'
        memory = f'RAM:{psutil.virtual_memory().percent}% SD:{psutil.disk_usage("/").percent}'
        boot_time = f'{datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d %H:%M")}'

        return f'cpu {cpu}\nmemory {memory}\n{boot_time}'
        value = f'{proces}\ncpu {cpu}\nmemory {memory}\n{boot_time}'

        self.logger.debug(f'{who_long(self)}: {proces_extra} {value}')
        return value
