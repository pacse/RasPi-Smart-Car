from .core import ADC
import time

from typing import Optional

class Photoresistor:
    def __init__(self):
        """Initialize the Photoresistor class"""
        self.adc = ADC()


    def read_left_photoresistor(self) -> Optional[float]:
        """
        Read the value from the left photoresistor.

        Returns:
            float: The voltage reading from the left photoresistor

            **None** if an error occurs.
        """
        try:
            return self.adc.read_adc(0)
        except Exception as e:
            print(f"Error reading left photoresistor: {e}")
            return None

    def read_right_photoresistor(self) -> Optional[float]:
        """
        Read the value from the right photoresistor.

        Returns:
            float: The voltage reading from the right photoresistor

            **None** if an error occurs.
        """
        try:
            return self.adc.read_adc(1)
        except Exception as e:
            print(f"Error reading right photoresistor: {e}")
            return None


    def cleanup(self) -> None:
        """Close the I2C bus."""
        self.adc.cleanup()


if __name__ == '__main__':
    """
    Test the Photoresistor class:
    Continuously read and print left & right
    photoresistor voltage values
    """
    print('Program is starting ... ')

    photoresistor = Photoresistor()

    try:
        while True:
            left_value = photoresistor.read_left_photoresistor()
            right_value = photoresistor.read_right_photoresistor()

            if left_value is not None and right_value is not None:
                print(f"The photoresistor L is {left_value}V, R is {right_value}V")

            time.sleep(0.3)

    except KeyboardInterrupt:
        print('\nEnd of program')

    finally:
        photoresistor.cleanup()
