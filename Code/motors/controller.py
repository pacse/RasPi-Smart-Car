from .car import Car
#from time import sleep

class Controller:
    """
    Adds Controller functionality to the Car class.
    """
    MAX = 30
    MIN = -30

    def __init__(self,
                 car: Car,
                 turn_scale: float = 0.75
                ) -> None:

        self.car = car
        self.TURN_SCALE = turn_scale


    def from_joystick(self, y_axis: float, x_axis: float) -> None:
        """
        Control the car using a single joystick.

        :param y_axis: Y-axis value from joystick (-100 to 100).
        :param x_axis: X-axis value from joystick (-100 to 100).
        """

        # Assumes y_axis and x_axis

        speed = round(y_axis)                   # forward/backward speed
        turn = round(x_axis * self.TURN_SCALE)  # turning adjustment
                                                # TURN_SCALE is sensitivity

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

        self.car.set_motor_speeds(FL = left_v, FR = right_v,
                                  BL = left_v, BR = right_v)
        #sleep(0.25)  # small delay to prevent overload


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

    def strafe_from_joystick(self, l_trigger, r_trigger) -> None:
        """
        Strafe the car left or right based on joystick input.

        :param l_trigger: Value of the left trigger (0 - 1).
        :param r_trigger: Value of the right trigger (0 - 1).
        """

        if l_trigger > r_trigger:
            l_trigger = round(l_trigger * 100)
            self.strafe_left(l_trigger)
        else:
            r_trigger = round(r_trigger * 100)
            self.strafe_right(r_trigger)

    def cleanup(self) -> None:
        """
        Cleanup the car's motors.
        """
        self.car.cleanup()
