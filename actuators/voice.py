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
    default_voice = {'amp': 100, 'speed': 150, 'gap': 5, 'pitch': 25}
    warning_voice = {'amp': 150, 'speed': 100, 'gap': 10, 'pitch': 5}

    def __init__(self) -> None:
        super().__init__(accepts=VoiceAction)
        self.voice = TTS(data={'engine': 'espeak', 'token': None, 'url': None})
        self.voice.espeak_params(**self.default_voice)
        self.actions = {'Ahoj': SayAhoy, 'Ja jsem Metro.': SayJaJsemMetro}


class SayAhoy(VoiceAction):
    def execute(self, actuator: Voice) -> None:
        actuator.voice.say('Ahoy!')


class SayJaJsemMetro(VoiceAction):
    def execute(self, actuator: Voice) -> None:
        actuator.voice.say('Ya ysem metro.')


class Say(VoiceAction):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def execute(self, actuator: Voice) -> None:
        actuator.voice.say(self.text)


class SayLowBattery(VoiceAction):
    def execute(self, actuator: Voice) -> None:
        actuator.voice.espeak_params(**actuator.warning_voice)
        actuator.voice.say('Prosim pomoc. Potrebuji nabit.')
        actuator.voice.espeak_params(**actuator.default_voice)
