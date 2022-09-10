from actuators import engine, terminal, repro, voice
from actuators.actuator import Actuator
from actuators.action import Priority
from controls.base import ControlBase
from controls.control1 import Control1
from controls.control2 import Control2
from controls.rc import RC
from lib.threading2 import LoggingExceptionsThread
from lib.utils import who, who_long
from sensors import battery, ultrasonic, psutil2
from config import Config

"""
    HW = sensors + actuators
    SW = sensor >DATA> control >ACTION> actuator
"""


class Control(ControlBase):
    """
        Archy Cortex.
        Main thread object wiring all the components together = car's brain.
         * Synchronously on main thread starts all components (each starts in its own thread) until the end when it stops them.
         * Asynchronously processing data for/from/on each sensor thread to trigger EMERGENCY level Actions like: FREEZE, COMA, DIE
         TODO: Detect engine movement with no distance traveled (obstacle or lift)
         TODO: Detect edge

         Command Pattern architecture:
         Command=Decision="Action" carries all the context (form where, why it was created and what should be done) needed to its processing.
         "Actions" are asynchronously created on several "Control" levels (each with its own execution priority and responsibility) as the system response to outside world provided by sensory data.
         "Actions" are synchronously processed by the "Actuators" based on the context they carrie, such is: Which Actuator can process, processing priority, ...
         "Actions" context also carrie when it was processed, with what result, how long did it took for consideration of another correcting Action/response.
    """

    def __init__(self) -> None:
        super().__init__(period=1, control=self)

        # actuators - processing actions - starts first - sorted by expected frequency of actions
        self.engine = engine.Engine()
        self.repro = repro.Repro()
        self.voice = voice.Voice()
        self.terminal = terminal.Terminal()

        # sensors - prerequisite for producing actions - start second
        self.battery = battery.Battery(period=10, control=self)
        self.ultrasonic = ultrasonic.Ultrasonic(period=0.5, control=self)
        self.psutil2 = psutil2.PsUtil(period=10)
        # TODO: CPUs load
        # TODO: CPU/APU temperatures
        # TODO: ds18x20 temperature

        # control - producing actions from sensory data - starting last
        self.control2 = Control2(period=1, control=self)    # neo cortex
        self.rc = RC(control=self)                          # remote controls web input/output
        self.control1 = Control1(period=0.5, control=self)  # paleo cortex
        # self                                              # archy cortex

        # all above
        self.components = [c for c in self.__dict__.values() if isinstance(c, LoggingExceptionsThread)]
        self.actuators = [c for c in self.__dict__.values() if isinstance(c, Actuator)]
        assert len(self.components) == 10
        assert len(self.actuators) == 4

        self.actions_kwargs = {'origin': self, 'priority': Priority.EMERGENCY, 'same_actions_limit': 1, 'abort_previous': True}

    def __enter__(self) -> None:
        self.logger.info(f'{who_long(self)} thread running, starting all the components:')
        [component.start() for component in self.components]

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.logger.info(f'{who_long(self)} thread ending, stopping all the components:')
        [component.stop() for component in self.components]
        [component.join() for component in self.components]
        self.logger.info(f'{who_long(self)}: not2b')

    def process_data(self, sensor) -> None:
        """ This method gets called asynchronously from each sensor thread. """
        self.logger.debug(f'{who_long(self)} processing: {who_long(sensor)}: {sensor.value}')
        action = {
            self.battery: terminal.ShutDown(duration=5, justification=f'Shutting down to save battery: {sensor.value} V.', **self.actions_kwargs) if sensor.value <= Config.VERY_LOW_VOLTAGE else None,
            self.ultrasonic: engine.Stop(duration=2, justification=f'Freezing car movement for 2s to not hit an obstacle: {sensor.value} cm.', **self.actions_kwargs) if sensor.value <= 4 else None,
        }.get(sensor, None)
        if action:
            self.perform(action)

    def perform_action(self, action: str, **kwargs) -> None:
        all_actions = (a for c in self.components for a in c.actions.values())
        for a in all_actions:
            self.logger.debug(f'{a.__name__} in {action} ?')
            if a.__name__ == action or f'.{a.__name__}' in action:
                kwargs['origin'].perform(action=a(**kwargs))    # origin control is responsible for creating this action
                return
        raise ValueError(f'Unknown action: {action}')

    def reverse_component_state(self, component: str) -> None:
        for c in self.components:
            if who(c) == component:
                c.reverse_activity()
                return
        raise ValueError(f'Unknown component: {component}')

    def main_loop(self) -> None:
        with self:
            while True:
                try:
                    self.iterate_wrapper()
                except KeyboardInterrupt:
                    self.logger.info(f'{who_long(self)} KeyboardInterrupt >> exiting')
                    break
                except Exception as ex:  # log & forget
                    self.last_exception = ex
                    self.logger.exception(f'{who_long(self)} FATAL ERROR IN THE MAIN LOOP:')
