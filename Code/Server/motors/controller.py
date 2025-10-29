from .car import Car
from time import sleep

class Controller:
    MAX = 30
    MIN = -30

    """
    Controller for the car's motors.
    """
    def __init__(self, car: Car) -> None:
        self.car = car


    def from_joystick(self, y_axis: float, x_axis: float) -> None:
        """
        Control the car using a single joystick.

        :param y_axis: Y-axis value from joystick (-100 to 100).
        :param x_axis: X-axis value from joystick (-100 to 100).
        """

        speed = round(y_axis)  # forward/backward speed
        turn = round(x_axis)   # turning adjustment

        left_v = speed - turn
        right_v = speed + turn

        # Clamp values to -100 to 100
        if left_v > self.MAX:
            left_v = self.MAX
        elif left_v < self.MIN:
            left_v = self.MIN

        if right_v > self.MAX:
            right_v = self.MAX
        elif right_v < self.MIN:
            right_v = self.MIN


        print("--- Joystick Input ---")
        print(f"Y-axis: {y_axis}, X-axis: {x_axis}")
        print(f'Speed: {speed}, Turn: {turn}')
        print(f"Left motor speed: {left_v}, Right motor speed: {right_v}")

        self.car.set_motor_speeds(FL = left_v, FR = right_v,
                                  BL = left_v, BR = right_v)
        sleep(0.25)  # small delay to prevent overload


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
