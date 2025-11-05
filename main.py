from Code.car_controller import Car_Controller
from Code import Car, Controller
from Code.config import MOTOR_PINS

# set up pygame for joystick handling
import pygame

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

car = Car(MOTOR_PINS)
controller = Controller(car)

car_controller = Car_Controller()

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
            controller.strafe_from_joystick(car_controller.trig_L, car_controller.Trig_R)
        #time.sleep(0.25)
finally:
    controller.cleanup()
    pygame.quit()
    print("Cleanup done.")

