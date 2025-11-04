from Code.motors import Motor
from Code.motors.car import Car
from Code.config import MOTOR_PINS

import time

car = Car(MOTOR_PINS)
car.set_motor_speeds(50, 50, 50, 50)

time.sleep(5)

car.set_motor_speeds(0, 0, 0, 0)

car.cleanup()
