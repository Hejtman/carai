from fakes.fake import Fake


class Ultrasonic(Fake):
    def __init__(self, trig, echo, timeout=0.02):
        super().__init__()
        self.logger.info(f'FAKE: Ultrasonic({trig=}, {echo=}, {timeout=})')

    def read(self, times=10):
        self.logger.info(f'FAKE: Ultrasonic.read')
        return -1


class Pin(Fake):
    def __init__(self, *value):
        super().__init__()
        self.logger.info(f'FAKE: Pin({value=})')

    def __call__(self, value):
        self.logger.info(f'FAKE: __call__({value=})')

    def value(self, *value):
        self.logger.info(f'FAKE: value({value=})')

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        self.logger.info(f'FAKE: mode({value=})')

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.logger.info(f'FAKE: irq({handler=}, {trigger=}, {bouncetime=})')

    def name(self):
        self.logger.info('FAKE: name')

    def names(self):
        self.logger.info('FAKE: names')
