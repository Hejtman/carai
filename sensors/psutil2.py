from sensors.sensor import Sensor
from lib.utils import who_long


import psutil


class PsUtil(Sensor):
    def __init__(self, period: float):
        super().__init__(period, store_last_values=1)
        self.psutil_process = psutil.Process()

    def read_raw_value(self) -> str:
        with self.psutil_process.oneshot():
            proces = f'{self.psutil_process.num_threads()}t {int(self.psutil_process.cpu_percent())}%'
        cpu1 = f'{int(psutil.cpu_percent(interval=None))}% '
        cpu2 = f'{int(psutil.cpu_freq(percpu=False).current)}GHz '\
               f'{int(psutil.sensors_temperatures().get("cpu_thermal")[0].current)}℃'
        memory = f'RAM:{int(psutil.virtual_memory().percent)}% '\
                 f'SD:{int(psutil.disk_usage("/").percent)}%'

        self.logger.debug(f'{who_long(self)}: {proces} {cpu1} {cpu2} {memory}')
        return f'{proces} {cpu1}<td colspan="100%">{cpu2} {memory}</td>'
