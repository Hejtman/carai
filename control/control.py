import logging
import time

from actuators import engine, terminal
from actuators.action import Priority
# noinspection PyUnresolvedReferences
from control import control2, control3, rc
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who
from sensors import battery, ultrasonic


class Control:
    """
        Archy Cortex.
        Main thread object wiring all components together - car's brain.
         * On main thread is running start / stop / monitor all the car's components - each work in its own thread
         * Asynchronously (process_data from component thread) triggered EMERGENCY level decisions > FREEZE, COMA, DIE > based on sensors direct reports
         TODO: Detect engine movement with no distance traveled (obstacle or lift)
         TODO: Detect edge
    """

    def __init__(self):
        # self                                                       # archy cortex
        self.control2 = control2.Control2(period=0.5, control=self)  # paleo cortex
        self.control3 = control3.Control3(period=1, control=self)    # neo cortex
        self.rc = rc.RC(control=self)                                # remote control localhost web input/output

        # sensors
        self.battery = battery.Battery(samples=10, period=10, control=self)
        self.ultrasonic = ultrasonic.Ultrasonic(samples=10, period=0.1, control=self)

        # actuators
        self.terminal = terminal.Terminal()
        self.engine = engine.Engine()

        # all above
        self.components = [c for c in self.__dict__.values() if isinstance(c, LoggingExceptionsThread)]
        assert len(self.components) == 7

        self.logger = logging.getLogger(__name__)
        self.priority = Priority.EMERGENCY
        self.watching_period = 1

        # DEBUG - to limit amount of logs
        self.battery.stop()

    def __enter__(self):
        self.logger.info(f'{who(self)} thread running, starting all the components:')
        for component in self.components:
            component.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f'{who(self)} thread ending, stopping all the components:')
        for component in self.components:
            component.stop()
        for component in self.components:
            component.join()
        self.logger.info(f'{who(self)}: not2b')

    def process_data(self, sensor):
        """ This method gets called asynchronously from each sensor thread. """
        self.logger.debug(f'{who(self)} processing: {who(sensor)}: {sensor.value}')

        match sensor:
            case self.battery:
                if sensor.value <= battery.VERY_LOW_VOLTAGE:  # DIE
                    self.perform(self.terminal, terminal.ShutDown(self.priority, 0), f'Shutting down the system to prevent battery damage do to low battery: {sensor.value} V.')

            case self.ultrasonic:
                if sensor.value <= 30:  # mm
                    self.perform(self.engine, engine.Stop(self.priority, 1), f'Freezing car movement for 1s to prevent damage do to obstacle distance: {sensor.value} cm.')

            case _:
                self.logger.error(f'Unhandled sensor: {who(sensor)}')

    def main_loop(self):
        """
            Watchdog running on main thread. Watching over components (living in separate threads) reporting as expected.
            No exception shall pass to the main().
        """
        with self:
            while True:
                # TODO: watching over sensors (and actuators processing given tasks?)
                # noinspection PyBroadException
                try:
                    time.sleep(self.watching_period)
                except KeyboardInterrupt:
                    self.logger.info(f'{who(self)} KeyboardInterrupt >> exiting')
                    break
                except:  # log & forget
                    self.logger.exception(f'{who(self)} FATAL ERROR IN THE MAIN LOOP:')

    def perform(self, actuator, action, log):
        if not actuator.current_action or action != actuator.current_action:
            self.logger.critical(log)
            actuator.put(action)
