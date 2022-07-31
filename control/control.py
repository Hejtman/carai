import logging
import time
from threading import Thread, Event


class Control(Thread):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.event_stop = Event()                   # to terminate the thread eventually
        self.sensors = None
        self.actuators = None
        self.watching_period = 1

    def __enter__(self):
        self.logger.info(f'{self.__class__.__name__} thread running, starting all the components:')
        for component in self.sensors + self.actuators:
            component.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f'{self.__class__.__name__} thread ended, stopping all the components:')
        for component in self.sensors + self.actuators:
            component.stop()

    def process_data(self, sensor):
        """ This method gets called asynchronously from each sensor thread. """
        self.logger.debug(f'processing:{sensor.__class__.__name__}\n')
        # TODO

    def run(self):
        """ Watchdog thread. Watching over sensors reporting in time as expected. """
        with self:
            while not self.event_stop.is_set():
                # TODO: watching over sensors (and actuators processing given tasks?)
                time.sleep(self.watching_period)

    def stop(self):
        """ Make the "Sensor reading and data processing thread" to finish. """
        self.event_stop.set()                               # Stop getting actions from the queue.


#SHUTDOWN_LEVEL = 3*2.6  # V
# from actuators.action import Priority
"""    def process_data(self):
        if self.value < SHUTDOWN_LEVEL:
            self.terminal.put(ShutDown(priority=Priority.EMERGENCY, duration=0), abort_current=True)
"""
