from .core import PCA9685

class Servo:
    """
    Servo motor controller using PCA9685 PWM driver.

    Handles up to 8 servo motors mapped to channels 8-15 on the PCA9685.
    Channel 0 is treated as a special case with reversed pulse calculation. (I wonder why?)
    """

    # constants
    PWM_FREQUENCY = 50     # Hz
    INITIAL_PULSE = 1500   # microseconds
    MIN_ANGLE     = 0      # degrees
    MAX_ANGLE     = 180
    VALID_MOTORS  = [i for i in range(0, 8)]

    # PWM constants
    MIN_PULSE   = 500      # microseconds
    MAX_PULSE   = 2500     # microseconds
    PULSE_RATIO = 0.09     # 4096 steps over 20ms


    def __init__(self):
        """Initialize the Servo controller."""

        try:
            self.pwm_servo = PCA9685(debug=True)
            self.pwm_servo.set_pwm_freq(self.PWM_FREQUENCY)

            for channel in self.VALID_MOTORS:
                self.pwm_servo.set_servo_pulse(channel + 8, self.INITIAL_PULSE)

        except Exception as e:
            raise RuntimeError('Failed to initialize servo controller.') from e


    # === validation ===
    def _validate_channel(self, channel: int) -> None:
        if channel not in self.VALID_MOTORS:
            raise ValueError((
                f'Invalid channel: {channel}. '
                f'Valid channels are {self.VALID_MOTORS}.'
            ))

    def _validate_angle(self, angle: int) -> None:
        if not self.MIN_ANGLE <= angle <= self.MAX_ANGLE:
            raise ValueError((
                f'Invalid angle: {angle}. '
                f'Valid angles are {self.MIN_ANGLE}-{self.MAX_ANGLE}.'
            ))

    def set_servo_pwm(self, channel: int, angle: int, error: int = 10) -> None:
        """
        Set servo position by angle.

        Args:
            channel: Servo channel (0-7)
            angle: Desired angle (0-180 degrees)
            error: Error correction value in degrees

        Raises:
            ValueError: If channel or angle is invalid
        """
        # validation
        channel = int(channel)
        angle = int(angle)
        self._validate_angle(angle)
        self._validate_channel(channel)

        # calculate pulse
        modifier = int((angle + error) / self.PULSE_RATIO)

        if channel == 0: # reversed logic for some reason
            pulse = self.MAX_PULSE - modifier

        else:
            pulse = self.MIN_PULSE + modifier

        # set pulse
        self.pwm_servo.set_servo_pulse((channel + 8), pulse)


    def cleanup(self) -> None:
        """Cleanup the servo controller."""
        self.pwm_servo.cleanup()


# Main program logic follows:
if __name__ == '__main__':
    """
    Test Servo class:
    Rotate servos 0 & 1 to 90 degrees.
    """
    print('Rotating servos to 90 degrees...')

    pwm_servo = Servo()

    try:
        while True:
            pwm_servo.set_servo_pwm(0, 90)
            pwm_servo.set_servo_pwm(1, 90)

    except KeyboardInterrupt:
        print('\nEnd of program.')
