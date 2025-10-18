from .__init__ import GPIO

class Buzzer:
    """
    Simple class to control a buzzer
    """
    def __init__(self) -> None:
        """Initialize the Buzzer class."""
        self.PIN = 17                   # Set buzzer pin #
        GPIO.setup(self.PIN, GPIO.OUT)  # Configure buzzer pin as output

    def on(self) -> None:
        """Turn on the buzzer."""
        GPIO.output(self.PIN, True)

    def off(self) -> None:
        """Turn off the buzzer."""
        GPIO.output(self.PIN, False)


    def close(self) -> None:
        """Cleanup the buzzer pin."""
        GPIO.cleanup(self.PIN)


if __name__ == '__main__':
    """
    Test the Buzzer class:
    turn on and off 3 times
    """
    import time

    print('Program is starting ... ')
    buzzer = Buzzer()
    try:
        for _ in range(3):
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.1)
    finally:
        buzzer.close()
