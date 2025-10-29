from Server.controller import Car_Controller
from Server.motors import Car, Controller
from Server.motors.config import MOTOR_PINS

import time

import pygame

pygame.init()
pygame.joystick.init()

car = Car(MOTOR_PINS)
controller = Controller(car)

# for motor in car.motors:
#     motor.set_speed(50)
#     time.sleep(2)
#     motor.set_speed(0)
# car.cleanup()

"""try:
    while True:
        car.forward(20)
finally:
    controller.cleanup()
    print("Cleanup done.")"""


# controller.from_joystick(1, 0)
# time.sleep(2)
# controller.from_joystick(0, 1)
# time.sleep(2)
# controller.strafe_left(50)
# time.sleep(2)
# controller.strafe_right(50)
# time.sleep(2)
# controller.cleanup()

car_controller = Car_Controller()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print(joysticks)


try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        car_controller.update()

        car_controller.display()
        if not car_controller.strafe:
            controller.from_joystick(-car_controller.pwm_y, -car_controller.pwm_x)
        else:
            controller.str
        #time.sleep(0.25)
finally:
    controller.cleanup()
    pygame.quit()
    print("Cleanup done.")

