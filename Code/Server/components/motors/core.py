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

    def __init__(self, pins: tuple[int, int], pwm_freq: int = 50) -> None:
        """
        Initialize the Motor controller.

        :param pins: Two BOARD pin numbers for forward and backward control.
        :param pwm_freq: The frequency for PWM control.
        """

        self.FORWARD, self.BACKWARD = pins

        GPIO.setup(pins, GPIO.OUT)

        # set up PWM for both directions
        self.pwm_forward = GPIO.PWM(self.FORWARD, pwm_freq)
        self.pwm_backward = GPIO.PWM(self.BACKWARD, pwm_freq)

        # prevent car moving on init
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)


    # === Validation ===
    def _validate_speed(self, speed: int) -> None:
        """Ensure speed is within valid range (0-100)."""
        if not (-100 <= speed <= 100):
            raise ValueError("Speed must be between -100 and 100")


    # === Control functions ===
    def change_speed(self, speed: int) -> None:
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
        self.change_speed(speed)

    def backward(self, speed: int) -> None:
        """
        Move the motor backward at the specified speed.

        :param speed: Speed percentage (0 - 100).
        """
        self.change_speed(-speed)


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
