from .. import GPIO

class Buzzer:
    """
    Control onboard buzzer using GPIO pin 11.
    """
    def __init__(self) -> None:
        """Initialize the Buzzer class."""
        self.PIN = 11                   # Set buzzer pin #
        GPIO.setup(self.PIN, GPIO.OUT)  # Configure buzzer pin as output

    def on(self) -> None:
        """Turn on the buzzer."""
        GPIO.output(self.PIN, True)

    def off(self) -> None:
        """Turn off the buzzer."""
        GPIO.output(self.PIN, False)


    def cleanup(self) -> None:
        """Cleanup the buzzer pin."""
        GPIO.cleanup(self.PIN)


if __name__ == '__main__':
    """
    Test the Buzzer class:
    turn on and off 3 times
    """
    from time import sleep

    print('Program is starting ... ')
    buzzer = Buzzer()
    try:
        for _ in range(3):
            buzzer.on()
            sleep(0.1)
            buzzer.off()
            sleep(0.1)

    except KeyboardInterrupt:
        print('\nEnd of program')

    finally:
        buzzer.cleanup()
