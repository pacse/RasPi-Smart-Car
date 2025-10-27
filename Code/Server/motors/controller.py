from .car import Car

class Controller:
    """
    Controller for the car's motors.
    """
    def __init__(self, car: Car) -> None:
        self.car = car


    def from_joystick(self, y_axis: int, x_axis: int) -> None:
        """
        Control the car using a single joystick.

        :param y_axis: Y-axis value from joystick (-1 to 1).
        :param x_axis: X-axis value from joystick (-1 to 1).
        """

        speed = round(y_axis * 100)  # forward/backward speed
        turn = round(x_axis * 100)   # turning adjustment

        left_v = speed + turn
        right_v = speed - turn

        self.car.set_motor_speeds(FL = left_v, FR = right_v,
                                  BL = left_v, BR = right_v)


    def strafe_left(self, speed: int) -> None:
        """
        Strafe the car left with mecanum wheels.

        :param speed: Speed percentage (0 - 100).
        """

        self.car.set_motor_speeds(FL = -speed, FR = speed,
                              BL = speed, BR = -speed)

    def strafe_right(self, speed: int) -> None:
        """
        Strafe the car right with mecanum wheels.

        :param speed: Speed percentage (0 - 100).
        """

        self.car.set_motor_speeds(FL = speed, FR = -speed,
                              BL = -speed, BR = speed)


    def cleanup(self) -> None:
        """
        Cleanup the car's motors.
        """
        self.car.cleanup()
