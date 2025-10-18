from .. import GPIO


class Infrared:
    """
    Handle IR sensors using GPIO pins
    8, 10, & 16 (Left, Middle, Right)
    """
    def __init__(self):
        """
        Initialize class and setup GPIO pins
        """

        self.IR_PINS = [8,10,16]  # Left, Middle, Right

        # Setup pins with pull-down resistors (may not be needed)
        for pin in self.IR_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def read_one_infrared(self, channel: int) -> int:
        """Read the value of a single infrared sensor."""

        # validate channel
        if channel not in [1, 2, 3]:
            raise ValueError(
                'Channel must be 1, 2, or 3 (Left, Middle, Right).'
            )

        pin = self.IR_PINS[channel - 1]  # Get corresponding pin
        return GPIO.input(pin)           # & read & return val

    def read_all_infrared(self) -> tuple[int, int, int]:
        """Read all IR sensor vals"""
        vals = []

        # iterate over all 3 sensors, reading values
        for i in range(0, 3):
            vals.append(GPIO.input(self.IR_PINS[i]))

        return (vals[0], vals[1], vals[2]) # Return as tuple


    def close(self) -> None:
        """Cleanup used GPIO pins."""
        for pin in self.IR_PINS:
            GPIO.cleanup(pin)


if __name__ == '__main__':
    """
    Test IR sensors:
    Continuously read and print all sensor values
    """
    from time import sleep

    # Create an Infrared object
    infrared = Infrared()
    try:
        # Continuously read and print the combined value of all infrared sensors
        while True:
            infrared_value = infrared.read_all_infrared()
            print(f"Infrared value: {infrared_value}")
            sleep(0.5)
    except KeyboardInterrupt:
        # Close the Infrared object and print a message when interrupted
        infrared.close()
        print("\nEnd of program")
