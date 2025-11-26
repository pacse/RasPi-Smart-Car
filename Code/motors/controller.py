from .car import Car


# are we testing or running?
testing = False


class Controller:
    """
    Adds Controller functionality to the Car class.

    :param car: The Car instance to control.
    :param turn_scale: Scaling factor for turning sensitivity. Default: 0.5
    """

    if testing:
        MAX = 30   # Max pwm duty cycle
        MIN = -30  # Min pwm duty cycle

    else:
        MAX = 100  # Max pwm duty cycle
        MIN = -100 # Min pwm duty cycle


    def __init__(self,
                 car: Car,
                 turn_scale: float = 0.5
                ) -> None:

        self.car = car
        self.TURN_SCALE = turn_scale

        print((
               f'Controller: MAX: {self.MAX}, '
               f'MIN: {self.MIN}, '
               f'TURN_SCALE: {self.TURN_SCALE}'
             ))


    def move_from_joystick(self, y_axis: float, x_axis: float) -> None:
        """
        Control the car from a joystick's input.

        :param y_axis: Y-axis value from joystick (-1 to 1).
        :param x_axis: X-axis value from joystick (-1 to 1).
        """

        # Assumes y_axis and x_axis are -1 to 1
        speed = round(y_axis * 100)                   # forward/backward speed
        turn = round(x_axis * 100 * self.TURN_SCALE)  # turning adjustment
                                                      # TURN_SCALE is sensitivity


        # Calculate speeds, clamping values to MIN/MAX
        left_v = min(self.MAX, max(self.MIN, speed - turn))
        right_v = min(self.MAX, max(self.MIN, speed + turn))


        # Set motor speeds
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
