from Code.Code.motors import Motor, config
from Code.Code.motors.car import Car
import time

car = Car(config.MOTOR_PINS)
car.set_motor_speeds(50, 50, 50, 50)

time.sleep(5)

car.set_motor_speeds(0, 0, 0, 0)

car.cleanup()
