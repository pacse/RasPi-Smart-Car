"""
Get input from a connected controller and display it in the terminal.
"""

import pygame

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print(joysticks)

class car:

    def __init__(self):
        self.accel_y = pygame.joystick.Joystick(0).get_axis(1)
        self.accel_x = pygame.joystick.Joystick(0).get_axis(0)
        self.trigger_l = pygame.joystick.Joystick(0).get_axis(4)
        self.trigger_r = pygame.joystick.Joystick(0).get_axis(5)
        self.pwm = 0 #pwm for motor >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> x
        self.pwm_y = 0
        self.pwm_trig_l = 0

    def display(self):     #can be turned into functions .... (but will be a hastle)
        #deadzone >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if 0< self.accel_x <= 0.2   or 0> self.accel_x >-0.2: self.acel_x = 0
        if 0< self.trigger_l <= 0.2   or 0> self.trigger_l >-0.2: self.trigger_l = 0
        if 0< self.trigger_r <= 0.2   or 0> self.trigger_r >-0.2: self.trigger_r = 0


        bar_length = 16      # total width of the bar
        marker_size = 5       # how wide the marker is
        pos = 1 # start centered
        #x>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        pos = int((self.accel_x + 1) /2  * (bar_length -1)) # the joysticj times the width of the #####  finds the center of where the start of the (x+1 to prevent negitives) /2 to find center x>>1 fx == 14 x>>2 fx == 29        (-1 to prevent it going off the bar)
        bar_1 = ['-'] * bar_length                          # creates a list for the ---######-----
        start = pos - marker_size //2                     # start of the ### - 1/2 of the marker size so it id centered correctly
        end = start + marker_size                         # end

        # keep marker inside the bar
        if start < 0:                                    # boundries (caps the movement to boundry so it cannot cross the border (...))
            start = 0
        if end > bar_length:
            end = bar_length

        for i in range(start, end):                    # for loop editing the list to insert the ### by saying start at the start value end at the end value
            bar_1[i] = '#'
        x_move =  "[" + "".join(bar_1) + "]"    # returnes characters [] boundries and joins the Bar list
        #y>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        pos = int(((self.accel_y*-1) + 1) /2  * (bar_length -1))
        bar_2 = ['-'] * bar_length                          # creates a list for the ---######-----
        start = pos - marker_size //2                     # start of the ### - 1/2 of the marker size so it id centered
        end = start + marker_size                         # end

        # keep marker inside the bar
        if start < 0:                                    # boundries
            start = 0
        if end > bar_length:
            end = bar_length

        for i in range(start, end):                    # for loop editing the list to insert the ### by saying start at the start value end at the end value
            bar_2[i] = '#'

        y_move =  "[" + "".join(bar_2) + "]"    # returnes characters [] boundries and joins the Bar list

        #trigger_r>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        pos = int(((self.trigger_l) + 1) /2  * (bar_length -1))
        bar_3 = ['-'] * bar_length                          # creates a list for the ---######-----
        start = pos - marker_size //2                     # start of the ### - 1/2 of the marker size so it id centered
        end = start + marker_size                         # end

        # keep marker inside the bar
        if start < 0:                                    # boundries
            start = 0
        if end > bar_length:
            end = bar_length

        for i in range(start, end):                    # for loop editing the list to insert the ### by saying start at the start value end at the end value
            bar_3[i] = '#'

        l_trig =  "[" + "".join(bar_3) + "]"    # returnes characters [] boundries and joins the Bar list

        #trigger_r>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        pos = int(((self.trigger_r) + 1) /2  * (bar_length -1))
        bar_4 = ['-'] * bar_length                          # creates a list for the ---######-----
        start = pos - marker_size //2                     # start of the ### - 1/2 of the marker size so it id centered
        end = start + marker_size                         # end

        # keep marker inside the bar
        if start < 0:                                    # boundries
            start = 0
        if end > bar_length:
            end = bar_length

        for i in range(start, end):                    # for loop editing the list to insert the ### by saying start at the start value end at the end value
            bar_4[i] = '#'

        r_trig =  "[" + "".join(bar_4) + "]"    # returnes characters [] boundries and joins the Bar list
        LB_pressed = pygame.joystick.Joystick(0).get_button(4)
        RB_pressed = pygame.joystick.Joystick(0).get_button(5)
        if self.accel_x < 0:
            self.pwm = self.accel_x*-1*100
        else:
            self.pwm = self.accel_x*100
        if self.accel_y < 0:
            self.pwm_y = self.accel_y*-1*100
        else:
            self.pwm_y = self.accel_y*100
        if self.trigger_l < 0:
            self.pwm_trig_l = self.trigger_l*-1*100
        else:
            self.pwm_y = self.accel_y*100
        x_y_info = f'L-R{x_move}PWR{y_move}L-TRIG{l_trig}R-TRIG{r_trig}LB_PRESSED={LB_pressed}__RB_PRESSED={RB_pressed}PWM_X[{round(self.pwm, 1):>5}]PWM_Y[{round(self.pwm_y, 1):>5}]'# info on what input is being displayed

        #t_size = os.get_terminal_size().columns

        #final = f'{x_y_info:^{t_size}}{r_trig}'
        #x_y_info = f'X_JOY_STRENGTH[{round(self.accel_x, 2):>7}], Y_JOY_SPEED[{round(self.accel_y, 2):>7}]{x_move}{y_move}'
        #print(' ' * t_size, end='\r')
        print(x_y_info, end='\r', flush=True)



    # Left Trigger
    # lt = controller.get_axis(4)
    # Right Trigger
    #rt = pygame.CONTROLLER_AXIS_TRIGGERRIGHT.g
    #key 0 >> A
    #key 1 >> B
    #key 2 >> X
    #key 3 >> Y
    #key 4 >> LB
    #key 5 >> RB
    #key 6 >> escape
    #key 7 >> menu
    #Key 8 >>
