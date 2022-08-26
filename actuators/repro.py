from abc import ABC
from actuators.action import Action
from actuators.actuator import Actuator


try:
    from robot_hat import Music  # noqa
except ModuleNotFoundError:
    from fakes.repro import Music


class MusicAction(Action, ABC):
    pass


class Repro(Actuator):
    def __init__(self) -> None:
        super().__init__(accepts=MusicAction)
        self.repro = Music()


class PlayX(MusicAction):
    def execute(self, actuator: Repro) -> None:
        actuator.repro.music_set_volume(80)
        actuator.repro.sound_play('X')
