from actuators.action import Action
from actuators.actuator import Actuator

from lib.utils import who


class Engine(Actuator):
    """
        * Performs drive / stop actions on the motors.
        * All motor actions are performed exclusively on the same thread to ensure serialisation / prioritisation.
    """
    default_speed = 1

    def __init__(self) -> None:
        super().__init__()
        self.speed = 0
        self.angle = 0
        self.previous_action = None
        self.latest_action = None

    def update_action(self, action: Action):
        self.previous_action = self.latest_action
        self.latest_action = action


class Start(Action):
    def execute(self, actuator: Engine) -> None:
        actuator.update_action(self)

        if self != actuator.previous_action:
            actuator.speed = Engine.default_speed
            # TODO: real engine start action
            self.logger.info(f'{who(actuator)} -> {who(self)} {actuator.speed=}')
        else:
            self.logger.debug(f'{who(actuator)} -> {who(self)} {actuator.speed=}')


class Stop(Action):
    def execute(self, actuator: Engine) -> None:
        actuator.update_action(self)

        if self != actuator.previous_action:
            actuator.speed = 0
            # TODO: real engine start action
            self.logger.info(f'{who(actuator)} -> {who(self)} {actuator.speed=}')
        else:
            self.logger.debug(f'{who(actuator)} -> {who(self)} {actuator.speed=}')


class SpeedUP(Action):
    def execute(self, actuator: Engine) -> None:
        self.logger.debug(f'{who(self)} Engine: Speeding UP {actuator.speed}+{Engine.default_speed}')
        actuator.update_action(self)
        actuator.speed += Engine.default_speed


class SlowDown(Action):  # TODO: negative / reverse?
    def execute(self, actuator: Engine) -> None:
        self.logger.debug(f'{who(self)} Engine: Slowing DOWN {actuator.speed}-{Engine.default_speed}')
        actuator.update_action(self)
        actuator.speed -= Engine.default_speed
