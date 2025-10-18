# this script is PMF and sacred, do not
# touch or you will have your hands cut off

import math
import smbus

from time import sleep
# ============================================================================
#                  Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:
    """
    PCA9685 16-channel PWM controller driver.

    This class provides an interface to the PCA9685 PWM controller,
    commonly used for controlling servos, motors, and LEDs.

    Args:
        address: I2C address of the PCA9685 (default: 0x40)
        debug: Enable debug output (default: False)

    Raises:
        OSError: If I2C communication fails
    """
    # Registers/etc.
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    # other constants
    CHANNELS = 16
    PWM_RESOLUTION = 4096    # 12-bit
    DEFAULT_FREQUENCY = 50   # Hz
    CLOCK_FREQ = 25000000.0  # 25MHz
    MIN_PULSE = 0
    MAX_PULSE = 20000        # microseconds

    def __init__(self, address: int = 0x40, debug: bool = False):
        """
        Initialize communication with PCA9685 at the specified I2C address.
        Default address is 0x40.
        """
        try:
            self.bus = smbus.SMBus(1)
            self.address = address
            self.debug = debug
            self.write(self.__MODE1, 0x00)
        except OSError as e:
            raise OSError(
                f'Failed to initialize PCA9685 at address {address:02x}'
            ) from e


    def write(self, reg: int, value: int) -> None:
        """Writes an 8-bit value to the specified register/address."""
        self.bus.write_byte_data(self.address, reg, value)

    def read(self, reg: int) -> int:
        """Read an unsigned byte from the I2C device."""
        result = self.bus.read_byte_data(self.address, reg)
        return result


    def set_pwm_freq(self, freq: float) -> None:
        """Sets the PWM frequency."""
        prescaleval = self.CLOCK_FREQ
        prescaleval /= self.PWM_RESOLUTION
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = math.floor(prescaleval + 0.5)

        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)


    def set_pwm(self, channel: int, on: int, off: int) -> None:
        """
        Sets a single PWM channel.

        Args:
            channel: Channel number (0-15)
            on: On time (0-4095)
            off: Off time (0-4095)

        Raises:
            ValueError: If parameters are out of range
        """

        # validation
        if not 0 <= channel <= 15:
            raise ValueError(
                f'Channel must be between 0 and 15 (Got {channel})'
            )
        if not 0 <= on <= 4095 or not 0 <= off <= 4095:
            raise ValueError((
                f'On and Off values must be between 0 and 4095'
                f'(Got On: {on}, Off: {off})'
            ))

        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def set_servo_pulse(self, channel: int, pulse: float) -> None:
        """Sets the Servo Pulse, The PWM frequency must be 50HZ."""
        pulse = pulse * 4096 / 20000        # PWM frequency is 50HZ, the period is 20000us
        self.set_pwm(channel, 0, int(pulse))


    def close(self) -> None:
        """Close the I2C bus."""
        self.bus.close()


if __name__=='__main__':
    pass


