"""
What this does (my best understanding):
Magic (don't ask where the IRD's are ¯\_(ツ)_/¯)

Credit to original authors and Claude Sonnet 3.5
for helping me understand and clarify the code
"""

import smbus                             # smbus for I2C communication
from ..parameter import ParameterManager  # ParameterManager class from the parameter module


class ADC:
    """
    Interface for ADS7830 Analog-to-Digital Converter.
    """

    # === Initialization ===

    # Class constants
    I2C_ADDRESS = 0x48            # I2C address of the ADS7830
    ADS7830_COMMAND = 0x84        # command byte for ADS7830
    MAX_CHANNEL = 7               # Maximum channel number for ADS7830
    VOLTAGE_COEFFICIENT_V1 = 3.3  # Voltage coefficient for PCB version 1
    VOLTAGE_COEFFICIENT_V2 = 5.2  # Voltage coefficient for PCB version 2

    def __init__(self) -> None:
        """Initialize the ADC class."""
        self.parameter_manager = ParameterManager()                  # Create a ParameterManager instance
        self.pcb_version = self.parameter_manager.get_pcb_version()  # Get the PCB version
        self.adc_voltage_coefficient = (                             # Set the ADC voltage coefficient
            self.VOLTAGE_COEFFICIENT_V1                              # based on the PCB version
            if self.pcb_version == 1
            else self.VOLTAGE_COEFFICIENT_V2
        )

        try:
            self.i2c_bus = smbus.SMBus(1)  # Initialize the I2C bus
        except OSError as e:
            raise RuntimeError(
                'Failed to initialize I2C bus. Ensure I2C is enabled on your device.'
                ) from e


    # === Helpers ===

    def _read_stable_byte(self, max_retries: int = 5) -> int:
        """
        Read a stable byte from the ADC with retry logic.

        Returns:
            int: Stable byte value read from ADC

        Raises:
            RuntimeError: If unable to get stable reading after max retries

        """

        for _ in range(max_retries):
            try:
                byte1 = self.i2c_bus.read_byte(self.I2C_ADDRESS)  # Read byte 1 from ADC
                byte2 = self.i2c_bus.read_byte(self.I2C_ADDRESS)  # Read byte 2 from ADC

                if byte1 == byte2:
                    return byte1                                  # Return value if both reads
            except OSError:                                       # are equal ignoring OSErrors
                continue

        raise RuntimeError(f'Failed to get stable reading from ADC after {max_retries}.')

    def _calculate_command_set(self, channel: int) -> int:
        """
        Calculate the command set for the ADS7830 ADC.

        Args:
            channel: The ADC channel (0-7)

        Returns:
            int: The calculated command set
        """
        # shift channel bits & combine
        shift_left = channel << 2           # eg. 0010 -> 1000
        shift_right = channel >> 1          # eg. 0010 -> 0001
        combined = shift_left | shift_right # eg. 1000 | 0001 -> 1001

        # only get last 3 bits
        masked = combined & 0x07            # eg. 1001 & 0111 -> 0001

        # final shift
        final = masked << 4

        # combine with base command and return
        return self.ADS7830_COMMAND | final


    # === Main Methods ===

    def read_adc(self, channel: int) -> float:
        """
        Read the ADC value for the specified channel.

        Args:
            channel: ADC channel number (0-7)

        Returns:
            float: Voltage reading in volts

        Raises:
            ValueError: If channel number is invalid
            RuntimeError: If I2C communication fails
        """

        # Validate channel number
        if channel < 0 or channel > self.MAX_CHANNEL:
            raise ValueError((
                f'Invalid channel number: {channel}. '
                f'Must be between 0 and {self.MAX_CHANNEL}.'
                ))

        try:
            command_set = self._calculate_command_set(channel)      # Calculate channel command set
            self.i2c_bus.write_byte(self.I2C_ADDRESS, command_set)  # Write the command set to the ADC
            value = self._read_stable_byte()                        # Read a stable byte from the ADC
            voltage = value / 255.0 * self.adc_voltage_coefficient  # Convert the ADC value to voltage

            return round(voltage, 2)                                # round voltage to 2dp. & return

        except OSError as e:
            raise RuntimeError('I2C communication with ADC failed.') from e

    def read_voltage(self) -> float:
        """
        Read the voltage from the power supply channel (channel 2)
        and returns the power value based on the PCB version.

        Returns:
            float: Voltage reading in volts
        """
        return self.read_adc(2) * (3 if self.pcb_version == 1 else 2)


    def scan_i2c_bus(self) -> list[int]:
        """
        Scan the I2C bus for connected devices.

        Returns:
            list[int]: List of found device addresses
        """

        found_devices = []                                         # Empty list for found addresses
        print('Scanning I2C bus...')
        for device in range(128):                                  # Iterate over possible I2C addresses (0 to 127)
            try:
                self.i2c_bus.read_byte_data(device, 0)             # Try to read data from current address
                found_devices.append(device)                       # Add address to list if successful
                print(f'Device found at address: 0x{device:02X}')  # Print address

            except OSError:
                pass                                               # Ignore OSErrors

        return found_devices                                       # Return found addresses

    def close_i2c(self) -> None:
        """Close the I2C bus."""
        self.i2c_bus.close()


if __name__ == '__main__':
    """
    Test the ADC class:
    Continuously read and print left & right
    photoresistor values & power voltage
    """
    from time import sleep

    print('Program is starting ... ')
    adc = ADC()                              # Create ADC class instance
    try:
        while True:
            try:
                left_idr = adc.read_adc(0)   # Read left photoresistor value
                right_idr = adc.read_adc(1)  # Read right photoresistor value
                power = adc.read_voltage()   # Read power voltage
                print((                      # Print values on one updating line
                    f'Left IDR: {left_idr}V, '
                    f'Right IDR: {right_idr}V, '
                    f'Power: {power}V'
                    ), end='\r', flush=True)

            except RuntimeError as e:        # Handle runtime errors
                print(f'Error reading ADC: {e}')

            sleep(1)                         # Wait 1s between reads

    except KeyboardInterrupt:
        print('\nStopping program...')

    finally:
        adc.close_i2c()                      # Ensure I2C bus is always closed
