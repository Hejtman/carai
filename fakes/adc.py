from fakes.fake import Fake


class ADC(Fake):
    def __init__(self, chn):
        super().__init__()
        self.logger.info(f'FAKE: ADC(chn={chn})')

    def read(self):
        self.logger.info(f'FAKE: ADC.read')
        return 99999999
