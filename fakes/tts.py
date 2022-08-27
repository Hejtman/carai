from fakes.fake import Fake


class TTS(Fake):
    def __init__(self, data):
        super().__init__()
        assert data['engine'] in ['espeak', 'gtts', 'polly']

    def _check_executable(self, executable):
        pass

    def say(self, words):
        pass

    def espeak(self, words):
        pass

    def gtts(self, words):
        pass

    def polly(self, words):
        pass

    def lang(self, *value):
        pass

    def supported_lang(self):
        pass

    def espeak_params(self, amp=None, speed=None, gap=None, pitch=None):
        pass
