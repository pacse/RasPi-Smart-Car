"""
Use motor class to create a full car (4 motors).
"""

from .core import Motor


class Car:
    """
    Individual motor control for a 4-wheeled car.
    """

    def __init__(self, motor_pins: list[tuple[int, int]]) -> None:
        """
        Initialize the Car class

        :param motor_pins: List of 8 BOARD pin numbers for 4 motors:\n
                           [(M1_forward, M1_backward),
                            (M2_forward, M2_backward),
                            (M3_forward, M3_backward),
                            (M4_forward, M4_backward)]

        :raises ValueError: If motor_pins does not contain exactly 4 tuples.
        """
        # validation

        if not (
                len(motor_pins) == 4 and # 4 motors
                all(isinstance(p, tuple) for p in motor_pins) # 4 tuples
               ):

            raise ValueError((
                '[Car CLASS - __init__]: motor_pins'
                ' must contain exactly 4 tuples.'
            ))


        self.FL_motor = Motor(motor_pins[0]) # front-left motor
        self.FR_motor = Motor(motor_pins[1]) # front-right motor
        self.BL_motor = Motor(motor_pins[2]) # back-left motor
        self.BR_motor = Motor(motor_pins[3]) # back-right motor

        # list for easy iteration
        self.motors = [
            self.FL_motor,
            self.FR_motor,
            self.BL_motor,
            self.BR_motor
        ]


    # === Base functions ===

    def set_motor_speeds(self, FL: int, FR: int, BL: int, BR: int) -> None:
        """
        Set speeds for all 4 motors.

        :param FL: Front-left motor speed (-100 to 100).
        :param FR: Front-right motor speed (-100 to 100).
        :param BL: Back-left motor speed (-100 to 100).
        :param BR: Back-right motor speed (-100 to 100).

        :raises ValueError: If speeds does not contain exactly 4 speed values.
        :raises RuntimeError: If setting any motor speed fails.
        """

        try:
            self.FL_motor.set_speed(FL)
            self.FR_motor.set_speed(FR)
            self.BL_motor.set_speed(BL)
            self.BR_motor.set_speed(BR)

        except Exception as e: # catch errors from motor class
            raise RuntimeError(f'Failed to set motor speeds:\n') from e

    def stop_all_motors(self) -> None:
        """
        Stop movement of all motors.
        """

        for motor in self.motors:
            motor.stop()


    def cleanup(self) -> None:
        """
        Clean up all motors.
        """

        for motor in self.motors:
            motor.cleanup()



    # === Base movement functions ===

    def forward(self, speed: int) -> None:
        """
        Move the car forward at the specified speed.

        :param speed: Speed percentage (0 - 100).
        """

        for motor in self.motors:
            motor.forward(speed)

    def backward(self, speed: int) -> None:
        """
        Move the car backward at the specified speed.

        :param speed: Speed percentage (0 - 100).
        """

        for motor in self.motors:
            motor.backward(speed)


    def turn_left(self, speed: int) -> None:
        """
        Turn the car left by running left motors backward and right motors forward.

        :param speed: Speed percentage (0 - 100).
        """

        self.set_motor_speeds(FL = -speed, FR = speed,
                              BL = -speed, BR = speed)

    def turn_right(self, speed: int) -> None:
        """
        Turn the car right by running right motors backward and left motors forward.

        :param speed: Speed percentage (0 - 100).
        """

        self.set_motor_speeds(FL = speed, FR = -speed,
                              BL = speed, BR = -speed)


    def pivot_left(self, speed: int) -> None:
        """
        Pivot the car left by stopping left motors and running right motors forward.

        :param speed: Speed percentage (0 - 100).
        """

        self.set_motor_speeds(FL = 0, FR = speed,
                              BL = 0, BR = speed)

    def pivot_right(self, speed: int) -> None:
        """
        Pivot the car right by stopping right motors and running left motors forward.

        :param speed: Speed percentage (0 - 100).
        """

        self.set_motor_speeds(FL = speed, FR = 0,
                              BL = speed, BR = 0)
