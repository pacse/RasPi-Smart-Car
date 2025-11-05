"""
Get input from a connected controller and display it in the terminal.
"""

import pygame as pg


def init_joystick(base_init = True, j_id = 0):
    """
    Initialize pygame and joystick module,
    and wait for a joystick to be connected.

    :param base_init: Whether to initialize pygame base modules.
    :param j_id: Joystick ID to connect to.

    :return: Initialized joystick object.
    """

    def _get_joystick():
        """
        Get needed joystick
        """
        print([pg.joystick.Joystick(x)
                         for x in range(pg.joystick.get_count())])
        count = pg.joystick.get_count()

        if count > j_id + 1:
            # get connected joysticks
            joysticks = [pg.joystick.Joystick(x)
                         for x in range(count)]

            # return the requested joystick
            return joysticks[j_id]

        else:
            return None


    # === init pygame if needed ===
    if base_init:
        pg.init()
        pg.joystick.init()


    # === wait for joystick connection ===
    joystick = _get_joystick()

    if not joystick:
        print("Waiting for joystick connection...")

    while not joystick:
        pg.time.wait(100)
        joystick = _get_joystick()

    print("Joystick connected.")

    joystick.init()
    return joystick

class Joystick_Handler:

    def __init__(self, joystick_id = 0, deadzone = 0.2):
        self.joystick_id = joystick_id
        self.joystick = init_joystick(j_id=joystick_id)
        self.deadzone = deadzone

        self.update()

    def reconnect(self):
        """
        Reconnect to joystick if disconnected.
        """

        self.joystick = init_joystick(False, self.joystick_id)

    def update(self):
        """
        Update joystick values.
        """

        # === helpers ===
        def _cap_val(val):
            if val < -1:
                return -1
            elif val > 1:
                return 1
            else:
                return val

        def _deadzone(
                      val: float,
                      zone: float = self.deadzone
                     ) -> float:

            if abs(val) < zone:
                return 0

            else:
                # scale output to account for deadzone
                if val > 0:
                    val -= zone
                else:
                    val += zone

                return val / (1 - zone)

        def _p_val(val: float) -> float:
            return _deadzone(_cap_val(val))

        # === get joystick values ===
        self.accel_y = self.joystick.get_axis(1)
        self.accel_x = self.joystick.get_axis(0)

        self.trig_L = self.joystick.get_axis(4)
        self.trig_R = self.joystick.get_axis(5)

        # self.L_Button = self.joystick.get_button(4)
        # self.R_Button = self.joystick.get_button(5)

        # === process values ===

        self.accel_x = _p_val(self.accel_x)
        self.accel_y = _p_val(self.accel_y)
        self.trig_L = _p_val(self.trig_L)
        self.trig_R = _p_val(self.trig_R)

        # remap triggers: -1 to 1  ->  0 to 1
        self.trig_L = (self.trig_L + 1) / 2
        self.trig_R = (self.trig_R + 1) / 2

        # is the car strafing?
        if self.trig_L > 0 or self.trig_R > 0:
            self.strafe = True
        else:
            self.strafe = False


    def display(self):     #can be turned into functions .... (but will be a hastle)

        bar_length = 16           # total width of the bar
        marker_size = 4           # how wide the marker is
        pos = 1                   # start centered
        bar = ['-'] * bar_length  # list for the bar characters

        def _render_bar(val):
            pos = int((val + 1) / 2 * (bar_length - 1))  # the joystick times the width of the #####  finds the center of where the start of the (x+1 to prevent negitives) /2 to find center x>>1 fx == 14 x>>2 fx == 29        (-1 to prevent it going off the bar)
            start = pos - marker_size // 2               # start of the ### - 1/2 of the marker size so it's centered correctly
            end = start + marker_size                    # end

            # keep marker inside the bar
            if start < 0:                               # boundaries (caps the movement to boundary so it cannot cross the border (...))
                start = 0
            if end > bar_length:
                end = bar_length

            for i in range(start, end):              # for loop editing the list to insert the ### by saying start at the start value end at the end value
                bar[i] = '#'

            return "[" + "".join(bar) + "]"         # returns characters [] boundaries and joins the Bar list

        # === x ===
        x_bar = _render_bar(self.accel_x)

        # === y ===
        y_bar = _render_bar(self.accel_y)

        # === trigger_l ===
        l_trig = _render_bar(self.trig_L)

        # === trigger_r ===
        r_trig = _render_bar(self.trig_R)


        # info on what input is being displayed
        # x_y_info = f'L-R{x_move}PWR{y_move}L-TRIG{l_trig}R-TRIG{r_trig}LB_PRESSED={self.L_Button}__RB_PRESSED={self.R_Button}PWM_X[{round(self.pwm_x, 1):>5}]PWM_Y[{round(self.pwm_y, 1):>5}]'
        x_y_info = f'L-R {x_bar} | PWR {y_bar} | L-TRIG {l_trig} | R-TRIG {r_trig}'

        # t_size = os.get_terminal_size().columns

        # final = f'{x_y_info:^{t_size}}{r_trig}'
        # x_y_info = f'X_JOY_STRENGTH[{round(self.accel_x, 2):>7}], Y_JOY_SPEED[{round(self.accel_y, 2):>7}]{x_move}{y_move}'
        #print(' ' * t_size, end='\r')
        print(x_y_info, end='\r', flush=True)



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
