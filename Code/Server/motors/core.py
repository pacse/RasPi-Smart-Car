"""
Core motor components

NOTE: Motors are controlled separately
from the rest of the board components.
"""
from ... import GPIO


class Motor:
    """
    Basic motor controller class.
    """

    def __init__(self, pins: tuple[int, int], pwm_freq: int = 100) -> None:
        """
        Initialize the Motor controller.

        :param pins: Two BOARD pin numbers for forward and backward control.
        :param pwm_freq: The frequency for PWM control. Default is 100Hz.
        """

        # === validation ===
        if len(pins) != 2:
            raise ValueError("pins must contain exactly 2 pin numbers.")

        if not all(isinstance(pin, int) for pin in pins):
            raise TypeError("All pin numbers must be integers.")

        if not all((1 <= pin <= 40) for pin in pins):
            raise ValueError("Pin numbers must be between 1 and 40.")


        # === setup ===

        self.FORWARD, self.BACKWARD = pins

        GPIO.setup(pins, GPIO.OUT)

        # set up PWM for both directions
        self.pwm_forward = GPIO.PWM(self.FORWARD, pwm_freq)
        self.pwm_backward = GPIO.PWM(self.BACKWARD, pwm_freq)

        # prevent car moving on init
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)


    # === Validation ===
    def _validate_speed(self, speed: int, min: int = -100, max: int = 100) -> None:
        """
        Ensure speed is within valid range (min-max).

        :param speed: Speed to validate.

        :param min: Minimum valid speed. Default: -100.
        :param max: Maximum valid speed. Default: 100.

        :raises TypeError: If speed is not an integer.
        :raises ValueError: If speed is not between min and max.
        """

        if not isinstance(speed, int):
            raise TypeError("Speed must be an integer")

        if not (min <= speed <= max):
            raise ValueError(f"Speed must be between {min} and {max}")


    # === Control functions ===
    def set_speed(self, speed: int) -> None:
        """
        Change the speed of the motor.

        :param speed: Speed percentage (-100 - 100).
        """

        self._validate_speed(speed)

        if speed > 0:
            self.pwm_backward.ChangeDutyCycle(0)
            self.pwm_forward.ChangeDutyCycle(speed)

        elif speed < 0:
            self.pwm_forward.ChangeDutyCycle(0)
            self.pwm_backward.ChangeDutyCycle(abs(speed))


    def forward(self, speed: int) -> None:
        """
        Move the motor forward at the specified speed.

        :param speed: Speed percentage (0 - 100).
        """
        self._validate_speed(speed, min=0, max=100)

        self.set_speed(speed)

    def backward(self, speed: int) -> None:
        """
        Move the motor backward at the specified speed.

        :param speed: Speed percentage (0 - 100).
        """
        self._validate_speed(speed, min=0, max=100)

        self.set_speed(-speed)


    def stop(self) -> None:
        """Stop the motor."""

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)


    def cleanup(self) -> None:
        """Clean up the GPIO settings for the motor."""

        self.stop()

        self.pwm_forward.stop()
        self.pwm_backward.stop()

        GPIO.cleanup(self.FORWARD)
        GPIO.cleanup(self.BACKWARD)
