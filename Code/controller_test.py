from Server.controller import Car_Controller
from Server.motors import Car, Controller
from Server.motors.config import MOTOR_PINS


import pygame

pygame.init()
pygame.joystick.init()

car = Car(MOTOR_PINS)
controller = Controller(car)

car_controller = Car_Controller()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print(joysticks)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #controller.from_joystick(car_controller.accel_x, car_controller.accel_y)
    print(car_controller.accel_x, car_controller.accel_y)
