import logging


class HW:
    logger = logging.getLogger(__name__)

    @staticmethod
    def set_speed(speed: float):
        HW.logger.info(f'setting {speed=}')
        # TODO:

    @staticmethod
    def set_steering_angle(angle: float):
        HW.logger.info(f'setting {angle=}')
        # TODO:
