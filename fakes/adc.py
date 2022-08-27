from fakes.fake import Fake


class ADC(Fake):
    def __init__(self, chn):
        super().__init__()
        self.logger.info(f'FAKE: ADC(chn={chn})')

    def read(self):
        self.logger.info(f'FAKE: ADC.read')
        return 999999

    def read_voltage(self):
        self.logger.info(f'FAKE: ADC.read_voltage')
        return 999999
