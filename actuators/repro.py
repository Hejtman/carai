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
        self.actions = {'⏹️': StopPlaying, 'Legends': PlayLegends}  # FIXME: can this be generic (all the MusicAction in this module)?


class StopPlaying(MusicAction):
    def execute(self, actuator: Repro) -> None:
        actuator.repro.music_stop()


class PlayLegends(MusicAction):
    def execute(self, actuator: Repro) -> None:
        # FIXME: VOLUME DOES NOT WORK
        #actuator.repro.background_music('/home/pi/music/00 - my-little-pony-legends-never-dies.mp3', loops=-1, start=0.0, volume=0.001)
        actuator.repro.music_set_volume(0.01)
        actuator.repro.sound_play('/home/pi/music/00 - my-little-pony-legends-never-dies.mp3')
