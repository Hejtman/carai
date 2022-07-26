from abc import ABC, abstractmethod
from actuators.action import Action
from actuators.actuator import Actuator

from lib.utils import who_long
from hw.motor2 import Motor

try:
    from robot_hat import Servo, PWM  # noqa
except ModuleNotFoundError:
    from fakes.servo import Servo, PWM


class EngineAction(Action, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute(self, actuator) -> None:
        self.logger.debug(f'{who_long(actuator)} -> {who_long(self)}: speed={actuator.speed} angle={actuator.angle}  {self.justification}')

        if actuator.is_different_action(self):  # execute the action, consume time, but perform change of engine configuration only when discontinuing previous action
            actuator.set_new_action(self)
            self.set(actuator)
            actuator.motors.wheel(speed=actuator.speed)
            actuator.direction.angle(angle=actuator.angle)

    @abstractmethod
    def set(self, actuator: Actuator) -> None:
        pass


class Engine(Actuator):
    """
        Allows robot to perform action which will move it from one location to another: MoveStraight, TurnLeft, Stop ...
        * Two motors + steering servo togather participate on the moving action.
        * All motor actions are performed exclusively on the same thread to ensure serialisation / prioritisation.
    """
    default_speed = 20

    def __init__(self) -> None:
        super().__init__(accepts=EngineAction)
        self.speed = 0
        self.angle = 0
        self.latest_action = None
        self.motors = Motor()
        self.direction = Servo(PWM('P2'))
        self.actions = {'◀️': TurnLeft,
                        '↔': TurnCenter,
                        '▶': TurnRight,
                        '▲': MoveStraight,
                        '▼': MoveBackwards,
                        '⏹': Stop}

    def set_new_action(self, action: Action):
        self.latest_action = action

    def is_different_action(self, action: Action):
        return self.latest_action != action


class TurnCenter(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.angle = 0


class MoveStraight(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.speed = Engine.default_speed
        actuator.angle = 0


class TurnLeft(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.angle = -30


class TurnRight(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.angle = 30


class Stop(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.speed = 0


class MoveBackwards(EngineAction):
    def set(self, actuator: Engine) -> None:
        actuator.speed = -Engine.default_speed
