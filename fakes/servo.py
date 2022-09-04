from fakes.fake import Fake


class Servo(Fake):
    def __init__(self, pwm):
        super().__init__()
        self.logger.info(f'FAKE: Servo(pwm={pwm})')

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        self.logger.info(f'FAKE: Servo(angle={angle})')
        assert -90 <= angle <= 90

    # pwm_value ranges MIN_PW 500 to MAX_PW 2500 degrees
    def set_pwm(self, pwm_value):
        self.logger.info(f'FAKE: Servo(pwm={pwm_value})')
        assert 500 <= pwm_value <= 2500


class PWM:
    def __init__(self, channel, debug="critical"):
        pass

    def i2c_write(self, reg, value):
        pass

    def freq(self, *freq):
        pass

    def prescaler(self, *prescaler):
        pass

    def period(self, *arr):
        pass

    def pulse_width(self, *pulse_width):
        pass

    def pulse_width_percent(self, *pulse_width_percent):
        pass


class Pin(PWM):
    def value(self, _):
        pass
