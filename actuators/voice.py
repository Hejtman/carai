from abc import ABC
from actuators.action import Action
from actuators.actuator import Actuator


try:
    from ezblock import TTS  # noqa
except ModuleNotFoundError:
    from fakes.tts import TTS


class VoiceAction(Action, ABC):
    pass


class Voice(Actuator):
    default_voice = {'amp': 100, 'speed': 175, 'gap': 5, 'pitch': 50}

    def __init__(self) -> None:
        super().__init__(accepts=VoiceAction)
        self.voice = TTS()
        self.voice.espeak_params(**self.default_voice)


class SayHellow(VoiceAction):
    def execute(self, actuator: Voice) -> None:
        actuator.voice.say('Kill all Humans!')
