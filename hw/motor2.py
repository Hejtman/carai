#!/usr/bin/env python3
try:
    from robot_hat.pwm import PWM  # noqa
    from robot_hat.pin import Pin  # noqa
except ModuleNotFoundError:
    from fakes.servo import PWM
    from fakes.servo import Pin


class Motor:
    PERIOD = 4095
    PRE_SCALER = 10

    def __init__(self):

        self.left_rear_pwm_pin = PWM('P13')
        self.right_rear_pwm_pin = PWM('P12')
        self.left_rear_dir_pin = Pin('D4')
        self.right_rear_dir_pin = Pin('D5')

        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]

        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRE_SCALER)

    def wheel(self, speed, motor=-1):
        direction = bool(speed > 0)
        speed = abs(speed)

        if speed:
            speed = int(speed / 2) + 50

        if motor == 0:
            self.left_rear_dir_pin.value(not direction)  # is only my HW wired this way?
            self.left_rear_pwm_pin.pulse_width_percent(speed)

        elif motor == 1:
            self.right_rear_dir_pin.value(direction)
            self.right_rear_pwm_pin.pulse_width_percent(speed)

        elif motor == -1:
            self.left_rear_dir_pin.value(not direction)  # is only my HW wired this way?
            self.left_rear_pwm_pin.pulse_width_percent(speed)
            self.right_rear_dir_pin.value(direction)
            self.right_rear_pwm_pin.pulse_width_percent(speed)
