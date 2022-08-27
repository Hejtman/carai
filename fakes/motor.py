from fakes.fake import Fake


class Motor(Fake):
    # motor 0,1,-1 aka both,
    # speed -100 ~ 100
    def wheel(self, speed, motor=-1):
        self.logger.info(f'FAKE: Motor.wheel(speed={speed} motor={motor})')
        assert -100 <= speed <= 100
        assert motor in [-1, 0, 1]
