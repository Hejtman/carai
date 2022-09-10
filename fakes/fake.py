import logging


class Fake:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('using FAKE!')
