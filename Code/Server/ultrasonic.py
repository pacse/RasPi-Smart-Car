from .. import GPIO

class Ultrasonic:
    """
    Ultrasonic distance sensor class using GPIO pins.
    """

    def __init__(self, trigger_pin: int = 27, echo_pin: int = 22, max_distance: float = 3.0):
        """
        Initialize the Ultrasonic sensor.
        """
        self.TRIG = trigger_pin  # Set the trigger pin number
        self.ECHO = echo_pin      # Set the echo pin number
        self.max_distance = max_distance  # Set the maximum distance

        self.sensor = DistanceSensor(echo=self.ECHO, trigger=self.TRIG, max_distance=self.max_distance)  # Initialize the distance sensor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_distance(self) -> float:
        """
        Get the distance measurement from the ultrasonic sensor.

        Returns:
        float: The distance measurement in centimeters, rounded to one decimal place.
        """
        try:
            distance = self.sensor.distance * 100  # Get the distance in centimeters
            return round(float(distance), 1)  # Return the distance rounded to one decimal place
        except RuntimeWarning as e:
            print(f"Warning: {e}")
            return None

    def close(self):
        # Close the distance sensor.
        self.sensor.close()  # Close the sensor to release resources

if __name__ == '__main__':
    # Initialize the Ultrasonic instance with default pin numbers and max distance
    with Ultrasonic() as ultrasonic:
        try:
            while True:
                distance = ultrasonic.get_distance()  # Get the distance measurement in centimeters
                if distance is not None:
                    print(f"Ultrasonic distance: {distance}cm")  # Print the distance measurement
                time.sleep(0.5)  # Wait for 0.5 seconds
        except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
            print("\nEnd of program")  # Print an end message
