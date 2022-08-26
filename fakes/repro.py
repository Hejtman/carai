from fakes.fake import Fake


class Music(Fake):
    @property
    def MUSIC_LIST(self):
        return []

    @property
    def SOUND_LIST(self):
        return []

    def note(self, n):
        pass

    def beat(self, b):
        return 0

    def tempo(self, *args):
        pass

    def sound_play(self, file_name):
        pass

    def sound_effect_play(self, file_name):
        pass

    def sound_effect_threading(self, file_name):
        pass

    def background_music(self, file_name, loops=-1, start=0.0, volume=50):  # -1:continue
        pass

    def music_set_volume(self, value=50):
        pass

    def music_stop(self):
        pass

    def music_pause(self):
        pass

    def music_unpause(self):
        pass

    def sound_length(self, file_name):
        pass

    def play_tone_for(self, freq, duration):
        pass
