"""
Get input from a connected controller and display it in the terminal.
"""

import pygame as pg

def _get_joystick(id: int):
    """
    return joystick object if connected, else None.
    """

    if pg.joystick.get_count() > id:
        return pg.joystick.Joystick(id)

    return None


def init_joystick(j_id = 0, base_init = True):
    """
    Initialize pygame and joystick module,
    and wait for a joystick to be connected.

    :param base_init: Whether to initialize pygame base modules.
    :param j_id: Joystick ID to connect to.

    :return: Initialized joystick object.
    """

    if base_init:
        pg.init()
        pg.joystick.init()


    # === wait for joystick connection ===
    joystick = _get_joystick(j_id)

    if not joystick:
        print("Waiting for joystick connection...")

        while not joystick:
            pg.time.wait(250)

            pg.joystick.quit()
            pg.joystick.init()

            joystick = _get_joystick(j_id)

    print("Joystick connected.")

    joystick.init()
    return joystick


class Joystick_Handler:

    # === display settings ===
    bar_width = 16
    marker_width = 4


    def __init__(self, joystick_id = 0, deadzone = 0.2):
        self.joystick_id = joystick_id
        self.joystick = init_joystick(j_id=joystick_id)
        self.deadzone = deadzone

        self.update()


    # === helpers ===
    def _deadzone(self, val: float) -> float:

        if abs(val) < self.deadzone:
            return 0

        else:
            # scale output to account for deadzone
            if val > 0:
                return (val - self.deadzone) / (1 - self.deadzone)

            return (val + self.deadzone) / (1 - self.deadzone)

    def _p_val(self, val: float) -> float:
        # clamp value between -1 and 1, then apply deadzone
        return self._deadzone(max(-1, min(1, val)))


    def _render_bar(self, val):

            # find center position of marker
            pos = int((val + 1) / 2 * (self.bar_width - 1))

            # find start and end positions of marker
            start = max(0, pos - self.marker_width // 2)
            end = min(self.bar_width, start + self.marker_width)


            # create & return bar
            left = '-' * start
            marker = '#' * (end - start)
            right = '-' * (self.bar_width - end)

            return f"[{left}{marker}{right}]"


    def reconnect(self):
        """
        Reconnect to joystick if disconnected.
        """

        # kill old joystick
        if self.joystick:
            self.joystick.quit()

        self.joystick = init_joystick(self.joystick_id, False)


    def update(self):
        """
        Update joystick values.
        """

        # === get & process joystick values ===
        self.accel_y = self._p_val(self.joystick.get_axis(1))
        self.accel_x = self._p_val(self.joystick.get_axis(0))

        # not using strafing for now
        # self.trig_L = self._p_val(self.joystick.get_axis(4))
        # self.trig_R = self._p_val(self.joystick.get_axis(5))

        self.L_Button = self.joystick.get_button(4)
        self.R_Button = self.joystick.get_button(5)


        # === process values ===

        # remap triggers: -1 to 1  ->  0 to 1
        # self.trig_L = (self.trig_L + 1) / 2
        # self.trig_R = (self.trig_R + 1) / 2

        # is the car strafing?
        # if self.trig_L > 0 or self.trig_R > 0:
        #     self.strafe = True
        # else:
        #     self.strafe = False


    def display(self):
        print(
            f'L-R {self._render_bar(self.accel_x)} | '
            f'PWR {self._render_bar(self.accel_y)}',
            end='\r',
            flush=True
        )



    # Left Trigger
    # lt = controller.get_axis(4)
    # Right Trigger
    #rt = pg.CONTROLLER_AXIS_TRIGGERRIGHT.g
    #key 0 >> A
    #key 1 >> B
    #key 2 >> X
    #key 3 >> Y
    #key 4 >> LB
    #key 5 >> RB
    #key 6 >> escape
    #key 7 >> menu
    #Key 8 >>
