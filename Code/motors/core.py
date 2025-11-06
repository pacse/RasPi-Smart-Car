"""
Core motor control class.
"""
from .. import GPIO


class Motor:
    """
    Core motor control class.

    :param pins: Two BOARD pin numbers for forward and backward control.
    :param pwm_freq: The frequency for PWM control. Default: 10kHz
    """

    def __init__(self,
                 pins: tuple[int, int],
                 pwm_freq: int = 10_000,
                 validating: bool = True # Are we validating inputs?
                                       # False for use with Car & Controller classes
                ) -> None:
        """
        Initialize the Motor controller.

        :param pins: Two BOARD pin numbers for forward and backward control.
        :param pwm_freq: The frequency for PWM control. Default: 10kHz
        :param validating: Whether to validate inputs. Default: True
        """

        # === Validation ===
        if validating:
            if len(pins) != 2:
                raise ValueError("pins must contain exactly 2 pin numbers.")

            if not all(isinstance(pin, int) for pin in pins):
                raise TypeError("All pin numbers must be integers.")

            if not all((1 <= pin <= 40) for pin in pins):
                raise ValueError("Pin numbers must be between 1 and 40.")

            if not isinstance(pwm_freq, int) or pwm_freq <= 0:
                raise ValueError("pwm_freq must be a positive integer.")


        # === Setup ===

        self.validating = validating
        self.FORWARD, self.BACKWARD = pins
        self.pins = pins

        GPIO.setup(self.pins, GPIO.OUT)

        # set up PWM for both directions
        self.pwm_forward = GPIO.PWM(self.FORWARD, pwm_freq)
        self.pwm_backward = GPIO.PWM(self.BACKWARD, pwm_freq)

        # prevent car moving on init
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)


    # === Validation func ===

    def _validate_speed(self, speed: int, min: int = -100, max: int = 100) -> None:
        """
        Ensure speed is within valid range (min-max).

        :param speed: Speed to validate.

        :param min: Minimum valid speed. Default: -100
        :param max: Maximum valid speed. Default: 100

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

        if self.validating:
            self._validate_speed(speed)


        self.pwm_forward.ChangeDutyCycle(max(0,  speed))
        self.pwm_backward.ChangeDutyCycle(max(0, -speed))


    def stop(self) -> None:
        """Stop the motor."""

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)


    def cleanup(self) -> None:
        """Clean up the GPIO pins for the motor."""

        # ensure motor is stopped
        self.stop()

        # stop PWM controllers
        self.pwm_forward.stop()
        self.pwm_backward.stop()

        # clean up GPIO pins
        GPIO.cleanup(self.pins)
