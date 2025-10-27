from gpiozero import Servo                     # type: ignore (not coding on Raspberry Pi)
from gpiozero.pins.pigpio import PiGPIOFactory # type: ignore (not coding on Raspberry Pi)

class SensorArrayServos:
    """
    Controller class for Camera & Ultrasonic sensor mount servos.
    """

    # === constants ===
    MIN_ANGLE       = 0         # degrees
    MAX_ANGLE       = 180
    INITIAL_ANGLE   = 90

    MIN_PULSE_WIDTH = 0.5/1000  # 500μs
    MAX_PULSE_WIDTH = 2.5/1000  # 2500μs

    VALID_MOTORS    = [0, 1]    # servo channels

    # GPIO pins for servos TODO: SET PINS
    SERVO_PINS = [
                  17,  # Servo 0 - Camera Pan
                  27,  # Servo 1 - Camera Tilt
                 ]


    def __init__(self):
        """Initialize Servo controller."""

        try:
            # pigpio factory gives precise control
            factory = PiGPIOFactory()

            self.servos = []

            for pin in self.SERVO_PINS:

                servo = Servo( # define gpiozero Servo instance
                    pin,
                    min_pulse_width=self.MIN_PULSE_WIDTH,
                    max_pulse_width=self.MAX_PULSE_WIDTH,
                    pin_factory=factory # use pigpio factory
                )

                servo.value = 0  # default to center (90°)

                self.servos.append(servo)

        except Exception as e:
            raise RuntimeError('Failed to initialize servos:\n') from e


    # === validation ===
    def _validate_channel(self, channel: int) -> None:
        if channel not in self.VALID_MOTORS:
            raise ValueError((
                f'Invalid channel: {channel}. '
                f'Valid channels are {self.VALID_MOTORS}.'
            ))

    def _validate_angle(self, angle: float) -> None:
        if not self.MIN_ANGLE <= angle <= self.MAX_ANGLE:
            raise ValueError((
                f'Invalid angle: {angle}. '
                f'Valid angles are {self.MIN_ANGLE}-{self.MAX_ANGLE}.'
            ))


    # === main methods ===
    def set_angle(self, channel: int, angle: float) -> None:
        """
        Set servo position by angle.

        :param channel: Servo channel (0-1)
        :param angle: Desired angle (0-180 degrees)

        :raises ValueError: If channel or angle is invalid
        """
        # validation
        self._validate_angle(angle)
        self._validate_channel(channel)

        # set servo position
        self.servos[channel].value = angle

    def set_joystick(self, x: float, y: float) -> None:
        """
        Sets servo positions based on joystick x and y values.

        :param x: Joystick x-axis value (-1.0 to 1.0)
        :param y: Joystick y-axis value (-1.0 to 1.0)

        :raises ValueError: If channel is invalid
        """

        # validation
        if not (-1.0 <= x <= 1.0):
            raise ValueError("x value must be between -1.0 and 1.0")

        if not (-1.0 <= y <= 1.0):
            raise ValueError("y value must be between -1.0 and 1.0")

        # map -1.0 - 1.0 to 0° - 180°
        x_val = (self.MAX_ANGLE / 2) * (x + 1)
        y_val = (self.MAX_ANGLE / 2) * (y + 1)

        self.set_angle(0, x_val)
        self.set_angle(1, y_val)

    def cleanup(self) -> None:
        """Cleanup the servos."""
        for servo in self.servos:
            servo.close()


def test():
    """
    Test SensorArrayServos class:
    Rotate servos to 90 degrees.
    """

    print('Rotating to 90 degrees...')

    servos = SensorArrayServos()

    try:
        while True:
            servos.set_angle(0, 90)
            servos.set_angle(1, 90)

    except KeyboardInterrupt:
        print('\nEnd of program.')
