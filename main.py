from Code.joystick_handler import Joystick_Handler
from Code import Car, Controller
from Code.config import MOTOR_PINS

import pygame as pg


# Initialize the car,
#                controller,
#                and joystick handler
car = Car(MOTOR_PINS)
controller = Controller(car)

joystick_handler = Joystick_Handler()


try:
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            elif event.type == pg.JOYDEVICEREMOVED:

                print("Joystick disconnected.")

                controller.car.stop_all_motors()
                joystick_handler.reconnect()

                print("Joystick reconnected.")


        joystick_handler.update()

        joystick_handler.display()
        if not joystick_handler.strafe:
            controller.from_joystick(-joystick_handler.accel_y, -joystick_handler.accel_x)
        else:
            controller.strafe_from_joystick(joystick_handler.trig_L, joystick_handler.trig_R)

finally:
    controller.cleanup()
    pg.quit()
    print("Cleanup done.")

